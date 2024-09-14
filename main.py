from flask import Flask,jsonify,request,abort
from flask_cors import CORS
from search_document import insert,search_
from flask_sqlalchemy import SQLAlchemy
from database_architecture import User
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = '"mysql://root:anup%406536@localhost/document_retrieval'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
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
    user_id = request.args.get("user_id")
    if check_user_limit(user_id):
        return jsonify({"error":"Rate limit exceeded"}),429
    query = request.args.get("text")
    k = request.args.get("text")
    return search_(query,k,user_id)

if __name__=="__main__":
    app.run()