# Document Retrieval System using Pinecone, LangChain, and Flask
This is a Flask-based document retrieval system built with Pinecone for vector search and LangChain for document processing. The application scrapes news articles, converts them into PDF format, and embeds them into a Pinecone vector database for efficient searching using OpenAI embeddings. The application also supports caching with Redis to improve performance for frequently queried search terms.

## Table of Contents
### Overview
Technologies Used
File Structure
Setup Instructions
Usage
Techniques Used
Pinecone Vector Search
Document Processing with LangChain
Caching with Redis
Rate Limiting
API Endpoints
Future Enhancements
Overview
This project is a full-stack document retrieval application that supports:

Scraping live news articles from the web.
Converting articles into PDF format.
Embedding document data into a vector database (Pinecone) for efficient retrieval based on similarity.
Searching through the stored documents using a custom query and threshold.
The core feature is the document search based on Pinecone’s vector database, enhanced by caching to reduce redundant processing. This project leverages several libraries, such as LangChain for document processing, Redis for caching, and Pinecone for vector search.

## Technologies Used
### Flask: 
Backend framework for handling API requests.
### Pinecone: 
A vector database to perform fast similarity searches on embeddings.
### LangChain:
Used for document processing (PDF splitting and chunking).
### Redis: 
In-memory cache for speeding up repetitive queries.
### SentenceTransformers: 
Used to generate embeddings from text using the all-MiniLM-L6-v2 model.
### MySQL: 
To store user information and limit the number of API calls per user.
### FPDF: 
For generating PDFs from scraped articles.
### NewsAPI: 
Used for scraping live news articles.
```
.
├── cache.py                # Redis-based caching implementation
├── main.py                 # The main Flask application
├── requirements.txt        # Python dependencies
├── scraping.py             # Script to scrape news and generate PDFs
├── search_document.py      # Handles document loading, embedding, and search
└── Dockerfile              # Docker setup for containerizing the application

```
## File Descriptions
### main.py:
This is the main entry point of the Flask application.
It handles HTTP requests and serves as the API layer.
The key functionalities include checking rate limits, querying the vector database, and caching results.
It also manages user interactions and logs the number of API calls per user using SQLAlchemy with MySQL as the database.

### search_document.py:
This file handles all document-related operations.
It loads PDF documents, chunks them into smaller text segments, and embeds them into the Pinecone database.
It provides search functionality where queries are embedded and matched against stored vectors using cosine similarity.

### scraping.py:
Responsible for scraping news articles from an external API (NewsAPI) and converting the content into PDFs.
Runs in a separate thread, periodically scraping new articles.
Each scraped article is saved as a PDF and uploaded to the Pinecone database after embedding.

### cache.py:
Implements caching functionality using Redis.
Speeds up frequent search queries by storing the results temporarily and retrieving them from the cache when available, reducing the need for repeated searches.

### Setup Instructions
1. Clone the repository
```
git clone <repository-url>
cd <repository-directory>
```
2. Install the required dependencies
```
pip install -r requirements.txt
```
3. Set up environment variables
You will need the following environment variables:
```
PINECONE_API_KEY: Your Pinecone API key for vector database operations.
NEWSAPIKEY: API key for fetching news articles from NewsAPI.
```
You can set them in a .env file or your system environment.

4. Initialize MySQL Database
Make sure to set up your MySQL database, and update the SQLALCHEMY_DATABASE_URI in main.py to point to your MySQL instance.

5. Run the application
python main.py
The app will be running at http://127.0.0.1:5000.

### Usage
Document Uploading:
When new PDFs are created by the scraper, they are automatically loaded into the Pinecone vector database for fast retrieval.
Search Functionality:
The /search endpoint lets you search through the embedded documents using a natural language query.
### Search Example:
```
curl -X GET 'http://127.0.0.1:5000/search?user_id=1&query=your-search-query&k=5&threshold=0.5'
```
This will return search results based on the vector similarity.

## Techniques Used
### Pinecone Vector Search
Pinecone is a fully-managed vector database optimized for similarity searches. By using it, we can store and search large volumes of document embeddings, ensuring quick retrieval of relevant documents. The system utilizes a SentenceTransformer model to generate embeddings for the documents, which are stored in the Pinecone index.

### Document Processing with LangChain
LangChain is used for processing PDF documents and splitting them into smaller chunks of text, which is crucial for generating embeddings that are small enough to be indexed efficiently. LangChain also helps handle multiple file formats and large documents by splitting them based on character length with overlap.

### Caching with Redis
Redis is used to cache search results, which optimizes the performance for repeated queries. Caching prevents redundant calls to Pinecone for previously requested queries, reducing response times for frequently asked questions.

### Rate Limiting
To prevent abuse of the API, rate limiting is enforced per user. This is managed using a MySQL database where the number of API calls per user is tracked. If a user exceeds the allowed number of calls (LIMIT), their subsequent requests are blocked.

### API Endpoints
Health Check
```
GET /health
Response: 200 OK if the API is operational.
```
Search Documents
```
GET /search
Parameters:
user_id: Unique identifier for the user.
query: Search query.
k: Number of top results to return.
threshold: Minimum similarity score to include results.
Response: JSON object containing the matching documents, with metadata and similarity scores.
```

