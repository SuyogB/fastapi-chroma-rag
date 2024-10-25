from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_chroma import Chroma
import warnings
import shutil
import os

warnings.filterwarnings('ignore')

# Function to create the database from a sample PDF
def create_db():

    if not os.path.exists(r"C:\Users\sbynd\interviewtest1\files\sample.pdf"):
        print("File does not exist.")
    else:
        loader = PyPDFLoader(r"C:\Users\sbynd\interviewtest1\files\sample.pdf")

    pages = loader.load()


    # Split the loaded text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100,length_function=len,
        is_separator_regex=False)
    chunks = text_splitter.split_documents(pages)
    print(len(chunks))

    ids = [str(i) for i in range(1, len(chunks) + 1)]

    # Initialize the embedding function
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Build the Chroma database using the documents and embeddings
    Chroma.from_documents(pages, embedding_function, persist_directory="chroma_db", ids=ids)


# Function to remove the existing database
def delete_persisted_db():
    if "chroma_db" in os.listdir():
        shutil.rmtree("chroma_db")
        print(f"Deleted database and its contents.")
    else:
        raise FileNotFoundError("Database not found.")