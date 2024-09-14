from flask import Flask,jsonify,request,abort
from flask_cors import CORS
from search_document import insert,search_
from flask_sqlalchemy import SQLAlchemy
from database_architecture import User
app = Flask(__name__)
CORS(app)
db = SQLAlchemy(app)
# with
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