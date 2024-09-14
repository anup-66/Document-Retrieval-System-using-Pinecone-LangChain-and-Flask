import os

import openai
import langchain
from pinecone import Pinecone,ServerlessSpec
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone as pd
from langchain.llms import OpenAI
from dotenv import load_dotenv
# Pinecone()
from sentence_transformers import SentenceTransformer


# from database_architecture import insert,search

def read_file(directory):
    file = PyPDFDirectoryLoader(directory)
    # print(file.load())
    document = file.load()
    return document

def chunking(docs,size = 1000,overlap = 60):
    split_ = RecursiveCharacterTextSplitter(chunk_size=size,chunk_overlap=overlap)
    docs = split_.split_documents(docs)
    return docs

doc = read_file("E:/21bce7985_ML/document_pdf/")
docs = chunking(docs=doc)
key = os.environ["OPENAI_API_KEY"]
# embedings = OpenAIEmbeddings(openai_api_key = key)
# print(embedings)
# ans = embedings.embed_query("how are you")
# print(ans)

model = SentenceTransformer('all-MiniLM-L6-v2')
def embed(model,docs):
    embedings =[]
    count = 0
    for doc in docs:
        # print(doc)
        count+=1
        for i in doc:
            # print(i)
            if i[0]=="metadata":
                continue
            # print(model.encode(i))
            embedings.append({"id":f"{count}","values":model.encode(i).tolist()[0]})
    return embedings

# print(len(model.encode(["hello how are you","o"]).tolist()[0]))
# Vector Db
pc = Pinecone(
    api_key ="ff392e8b-ee20-4d42-8b41-deea1a96a624",
    # region = "us-east-1"
)

# print(embed(model,docs))
index_name = "ragllm"
index = pc.Index(index_name)
def upload_data(index_name,pc):

    # index = pc.create_collection(docs,model,index_name=index_name)
    index.upsert(vectors = embed(model,docs),namspace="collection1")
    print(index)
def query(index,query,k,threshold):
    res = index.query(
        namespace = "collection1",
        vector = model.encode(query).tolist()[0],
        top_k = 5,
        include_values = True,
        include_metadata = True
    )
    return res
print(query(index,"We have three primary different types of dish available.",3,0.23))
# def add_document(title,content):
#     embedding = model.encode(content).tolist()
#     insert(title,content)
#     return {"title":title,"message":"Document added"}
#
# def search_(query,k,limit):
#     search_vec = model.encode(query).tolist()
#     results = search(search_vec,k,limit)
#
#     return results
