# import json
# #
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
#
# import weaviate
# import weaviate.classes as wvc
# from weaviate.classes.query import MetadataQuery
# # client = weaviate.Client("http://localhost:8080")
# client = weaviate.connect_to_local()
# print(client.is_ready())
#
# try:
#     documents = client.collections.create(
#         name = "News",
#         vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_transformers(),
#         properties = [
#             wvc.config.Property(
#                 name = "title",
#                 data_type = wvc.config.DataType.TEXT,
#             ),
#             wvc.config.Property(
#                 name="content",
#                 data_type = wvc.config.DataType.TEXT,
#             ),
#         ]
#     )
#     print("schema created.")
# finally:
#     client.close()
# def insert(title,text):
#     properties= json.loads({"title":title,"content":text})
#     # news_obj = list()
#     # news_obj.append(
#     #     {
#     #         "title":properties
#     #     }
#     # )
#     news = client.collections.get("News")
#     news.data.insert(properties)
#
# insert("there is a big fest to be organised in bihar","many people will be comming to bihar for the big fest that is going to be organised by aisec organisation.")
# def search(query,k,max_dist):
#     news = client.collections.get("News")
#     response = news.query.near_text(
#         query = query,
#         limit = k,
#         return_metadata = MetadataQuery(distance = True)
#     )
#     return response.objects[0].properties
#
# db = SQLAlchemy()
# class User(db.Model):
#     id = db.Column(db.Integer,primary_key =True)
#     user_id = db.Column(db.Integer,unique =True,nullable = False)
#     api_calls = db.Column(db.Integer,default=1)
#     logs = db.Column(db.DateTime,default = datetime.utcnow)
#
#
# # class Document(db.Model):
# #     id = db.Column(db.Integer,primary_key = True)
# #     title = db.Column(db.String(100))
# #     paragraph = db.Column(db.Text,nullable = False)
# #     embedding = db.Column(db.Text,nullable = False)
# #     logs = db.Column(db.DateTime,dafault = datetime.utcnow)
# #
# #     def save_embed(self,embedding):
# #         self.embedding = json.dumps(embedding)
# #
# #     def get_embed(self):
# #         return json.loads(self.embedding)
