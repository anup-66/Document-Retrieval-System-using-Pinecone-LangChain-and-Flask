from flask import Flask,jsonify,request,abort
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/health",methods = ["GET"])
def health():
    return jsonify({"status":"API is ready to serve"}),200

if __name__=="__main__":
    app.run()