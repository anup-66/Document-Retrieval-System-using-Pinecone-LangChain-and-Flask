import os
import time
from flask import Flask, jsonify, request, abort, render_template
from flask_cors import CORS
from search_document import query,read_single_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pinecone import Pinecone
from cache import get_cache,set_cache
from transformers import pipeline
from scraping import Scraper
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:anup%406536@localhost/document_retrieval"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["LIMIT"] = 5
app.config["PINECONE_API_KEY"] = os.environ.get(
    "PINECONE_API_KEY"
)
db = SQLAlchemy(app)
pc = Pinecone(
    api_key =app.config["PINECONE_API_KEY"],
)

index_name = "ragllm"
index = pc.Index(index_name)
class User(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    user_id = db.Column(db.Integer,unique =True,nullable = False)
    api_calls = db.Column(db.Integer,default=1)
    logs = db.Column(db.DateTime,default = datetime.utcnow)

with app.app_context():
    db.create_all()

def check_user_limit(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    flag = False
    if not user:
        user = User(user_id=user_id,api_calls = 1)
        db.session.add(user)
    else:
        if user.api_calls>=app.config["LIMIT"]:
            flag = True
            abort(429,description="Rate limit Exceeded")
        user.api_calls+=1
    db.session.commit()
    return flag
@app.route("/health",methods = ["GET"])
def health():
    return jsonify({"status":"API is ready to serve"}),200

@app.route("/search",methods = ["GET"])
def find():
    user_id = request.args.get("user_id",None)
    q = request.args.get("query","")
    k = request.args.get("k",5,type=int)
    threshold = request.args.get("threshold",0.5,type=float)

    if check_user_limit(user_id):
        return jsonify({"error":"Rate limit exceeded"}),429
    start_time = time.time()
    cache_key = str(f"{user_id}:{q}")
    # print(cache_key)
    cache_res = get_cache(cache_key)
    if cache_res:
        return render_template('index.html',data = jsonify(cache_res),time = (time.time()-start_time))
    start_time = time.time()
    result = query(index,q,k,threshold)

    filtered_data = {"matches":[match for match in result['matches'] if match['score'] > threshold]}

    """ if it is needed to use this for Inference ."""
    answer = get_response(filtered_data,q)
    set_cache(key=cache_key,value = str(filtered_data))
    return render_template('index.html', data=filtered_data,time = (time.time()-start_time),answer=answer)
import google.generativeai as genai
import os
def get_response(filtered_data,query):
    pdf_file = filtered_data.get("matches")[0].get("metadata").get("source")
    context = read_single_file(pdf_file)
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    modal = genai.chat(model='models/chat-bison-001',
                       temperature=0.25,
                       top_p=0.95,
                       top_k=40, context=context,
                       messages=f"Based on the given context Answer the question,question:{query}")

    return modal.messages[-1]
def retrieve_inference(filtered_data,query):
    pdf_file = filtered_data.get("matches")[0].get("metadata").get("source")
    context = read_single_file(pdf_file)
    generator = pipeline("text-generation",model = "gpt2")
    response = generator(f"Question:{query}\ncontext:{context}\nAnswer:",max_length=150,num_return_sequence =1)
    return response[0]["generates_text"]

if __name__=="__main__":
    scraper = Scraper()
    scraper.start()
    app.run(debug=True)