from fastapi import FastAPI, HTTPException
from models import Query
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from functions import create_db, delete_persisted_db

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Fast API at work!"}

# Endpoint to create the database
@app.get("/create/")
async def create_database():
    create_db()
    return {"message": "Database successfully created."}

# Endpoint to delete the database
@app.delete("/delete/")
async def delete_database():
    try:
        delete_persisted_db()
        return {"message": "Database has been deleted."}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# Endpoint to fetch similar items based on the query
@app.post("/neighbours/")
async def fetch_item(query: Query):
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="chroma_db",embedding_function=embedding_function)
    results = db.similarity_search(query.query, k=query.neighbours)
    return {"message": "Nearest neighbours found.", "results": results}