import os

from pinecone import Pinecone
from langchain.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from sentence_transformers import SentenceTransformer

pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY")
)

index_name = "ragllm"
index = pc.Index(index_name)
model = SentenceTransformer('all-MiniLM-L6-v2')

#To read a all files in directory
def read_files(directory):
    file = PyPDFDirectoryLoader(directory)
    document = file.load()
    return document

# To generate embeding from the documents
def embed(model, docs,count):
    embeddings = []
    for doc in docs:
        count += 1
        metadata = doc.metadata
        content = doc.page_content
        embedding_values = model.encode(content).tolist()

        embeddings.append({
            "id": f"{count}",
            "values": embedding_values,
            "metadata": metadata
        })
    return embeddings

# To generate chunks from the documents
def chunking(docs, size=100, overlap=60):
    split_ = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    docs = split_.split_documents(docs)
    return docs

# To read and add embedding to the VectorDb Pinecone
def read_single_file(file_path):
    file = PyPDFLoader(file_path)
    document = file.load()
    document = chunking(document)
    str_ = ""
    for doc in document:
        str_+=doc.page_content
    return str_

# To load single file to the Pinecone Vector Database
def single_file_loading(file, size=1000, overlap=60,count=1):
    file = PyPDFLoader(file)
    # print(file)
    document = file.load()
    # print(document)
    document = chunking(document)
    embeding = embed(model, document,count)
    # return embeding
    index.upsert(vectors=embeding, namespace="collection1")

# To load Multiple files from the directory to the Vector Database
def data_loading(directory):
    doc = read_files(directory)
    docs = chunking(docs=doc)
    embeding = embed(model, docs)
    index.upsert(vectors=embeding, namespace="collection1")

# To get the top K queries from the vector database to be returned for llm response
def query(index, q, k, threshold):
    res = index.query(
        namespace="collection1",
        vector=model.encode(q).tolist(),
        top_k=k,
        include_values=True,
        include_metadata=True
    )

    return res