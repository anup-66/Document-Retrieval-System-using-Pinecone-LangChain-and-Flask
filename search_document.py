from sentence_transformers import SentenceTransformer
from database_architecture import insert,search
model = SentenceTransformer('all-MiniLM-L6-v2')

def add_document(title,content):
    embedding = model.encode(content).tolist()
    insert(title,content)
    return {"title":title,"message":"Document added"}

def search_(query,k,limit):
    search_vec = model.encode(query).tolist()
    results = search(search_vec,k,limit)

    return results