
import weaviate
client = weaviate.Client("http://localhost:8080")
schema = \
{
    "classes":
        {
            "class":"Document",
            "Preoperties":[
                {"name":"title","dataType":["string"]},
                {"name":"content","datatype":["text"]},
                {"name":"embedding","datatype":["number[]"],
                 "vectorIndexType":"hnsw","vectorizer":"text2vex-transformers"}
            ]
        }
}

if not client.schema.exists("Document"):
    client.schema.create(schema)

def insert(title,text,embedding):
    properties= {"title":title,"content":text,"embedding":embedding}
    client.data_object.create(properties,"Document")

def search(query,k,max_dist):
    return client.query.get("Document",["title","content"])\
                .with_near_vector({"vector":query,"distance":max_dist}).with_additional(["distance"]).with_limit(k).do()


# import json
#
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# db = SQLAlchemy()
# class User(db.Model):
#     id = db.Column(db.Integer,primary_key =True)
#     user_id = db.Column(db.Integer,unique =True,nullable = False)
#     api_calls = db.Column(db.Integer,default=1)
#     logs = db.Column(db.DateTime,default = datetime.utcnow)
#
# class Document(db.Model):
#     id = db.Column(db.Integer,primary_key = True)
#     title = db.Column(db.String(100))
#     paragraph = db.Column(db.Text,nullable = False)
#     embedding = db.Column(db.Text,nullable = False)
#     logs = db.Column(db.DateTime,dafault = datetime.utcnow)
#
#     def save_embed(self,embedding):
#         self.embedding = json.dumps(embedding)
#
#     def get_embed(self):
#         return json.loads(self.embedding)
