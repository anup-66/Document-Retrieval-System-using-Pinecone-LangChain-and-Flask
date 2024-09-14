from pinecone import Pinecone
from langchain.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from sentence_transformers import SentenceTransformer

pc = Pinecone(
    api_key="ff392e8b-ee20-4d42-8b41-deea1a96a624"
)

# print(embed(model,docs))
index_name = "ragllm"
index = pc.Index(index_name)
model = SentenceTransformer('all-MiniLM-L6-v2')


def read_file(directory):
    file = PyPDFDirectoryLoader(directory)
    document = file.load()
    return document


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


def chunking(docs, size=100, overlap=60):
    split_ = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    docs = split_.split_documents(docs)
    return docs


def single_file_loading(file, size=1000, overlap=60,count=1):
    file = PyPDFLoader(file)
    # print(file)
    document = file.load()
    # print(document)
    document = chunking(document)
    embeding = embed(model, document,count)
    # return embeding
    index.upsert(vectors=embeding, namespace="collection1")
#

def data_loading(directory):
    doc = read_file(directory)
    docs = chunking(docs=doc)
    embeding = embed(model, docs)
    index.upsert(vectors=embeding, namespace="collection1")

# print(model.encode("European iPad users can soon download apps from third-party stores ").tolist())
def query(index, q, k, threshold):
    res = index.query(
        namespace="collection1",
        vector=model.encode(q).tolist(),
        top_k=5,
        include_values=True,
        include_metadata=True
    )

    return res