# import numpy as np
# from sentence_transformers import SentenceTransformer
# # from database_architecture import Document
# class Search:
#     def __init__(self):
#         self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
#
#     def cosine(self,vec1,vec2):
#         return np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))
#
#     def search(self,text,limit = 5,threshold = 0.5):
#         embed = self.encoder.encode(text).tolist()
#         document = Document.query.all()
#         results = []
#         for doc in document:
