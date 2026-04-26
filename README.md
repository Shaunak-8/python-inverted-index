# FastAPI Inverted Index Search Engine

A high-performance, full-stack custom search engine built from scratch using Python, FastAPI, and PostgreSQL. 

Instead of relying on out-of-the-box solutions like Elasticsearch, this project features a custom-built **inverted index** and implements the **BM25 ranking algorithm** for highly relevant text retrieval, paired with NLP capabilities using NLTK and spaCy.

## 🚀 Features

- **Custom Search Core:** Hand-rolled inverted index and query processor.
- **Advanced Ranking:** Implements the BM25 algorithm (TF-IDF evolution) for accurate document scoring and relevance.
- **NLP Pipeline:** Tokenization, stemming, and lemmatization using `nltk` and `spacy`.
- **High-Performance API:** Asynchronous REST API built with FastAPI.
- **Robust Storage:** PostgreSQL database integration using SQLAlchemy and Alembic for data persistence and metadata.
- **Caching Ready:** Redis integration for high-speed query response caching.
- **Dockerized:** Fully containerized backend, database, and cache via `docker-compose` for seamless local development.

## 🛠️ Technology Stack

- **Backend Framework:** FastAPI, Pydantic
- **Search & NLP:** NLTK, spaCy, Custom BM25 Ranker
- **Database:** PostgreSQL, SQLAlchemy (ORM), Alembic (Migrations)
- **Caching:** Redis
- **Containerization:** Docker, Docker Compose

## 📂 Architecture

```
backend/
├── app/
│   ├── api/             # FastAPI route definitions (search, documents, analytics)
│   ├── core/            # App configurations and settings
│   ├── data/            # Data storage/models
│   ├── db/              # Database connection and setup
│   ├── search_engine/   # Core search logic
│   │   ├── indexer.py         # Document indexing logic
│   │   ├── inverted_index.py  # Inverted index data structure
│   │   ├── query_processor.py # Query parsing and NLP
│   │   └── ranker.py          # BM25 scoring algorithm
│   └── main.py          # Application entry point
├── Dockerfile           # Backend container definition
└── requirements.txt     # Python dependencies
```

## 🚦 Getting Started

### Prerequisites
- Docker and Docker Compose installed on your machine.

### Running the App Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/fastapi-search-engine.git
   cd fastapi-search-engine
   ```

2. **Start the services via Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the API:**
   - The FastAPI backend will be running at `http://localhost:8000`
   - Access the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`

## 🧠 How It Works

1. **Document Ingestion:** When a document is added via the `/documents` API, the NLP pipeline processes the text (tokenization, removing stop words, lemmatization).
2. **Indexing:** The processed terms are added to the custom Inverted Index, mapping terms to document IDs and their positions.
3. **Querying:** When a user searches via the `/search` API, the query is processed using the same NLP pipeline.
4. **Ranking:** The `BM25Ranker` scores the indexed documents based on term frequency, inverse document frequency, and document length normalization, returning the most relevant results instantly.

## 📄 License

This project is open-source and available under the MIT License.
