import time

from flask import Flask, jsonify, request, abort, render_template
from flask_cors import CORS
from search_document import query
from flask_sqlalchemy import SQLAlchemy
# from database_architecture import User
from datetime import datetime
from pinecone import Pinecone
from cache import get_cache,set_cache
from scraping import Scraper

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:anup%406536@localhost/document_retrieval"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["LIMIT"] = 5
db = SQLAlchemy(app)
pc = Pinecone(
    api_key ="ff392e8b-ee20-4d42-8b41-deea1a96a624",
    # region = "us-east-1"
)

# print(embed(model,docs))
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
        return jsonify({"message":str(cache_res),"time":(time.time()-start_time)}),200
    start_time = time.time()
    result = query(index,q,k,threshold)
    set_cache(key=cache_key,value = str(result))
    # print(result)
    return render_template('index.html', data=result)
    # return jsonify({"messsage":result,"time":time.time()-start_time})

if __name__=="__main__":
    # scraper = Scraper()
    # scraper.start()
    app.run(debug=True)