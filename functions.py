from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
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

    # Specify the file paths for different document types
    pdf_path = r"C:\Users\sbynd\interviewtest2\files\sample.pdf"
    docx_path = r"C:\Users\sbynd\interviewtest2\files\sample.docx"
    txt_path = r"C:\Users\sbynd\interviewtest2\files\sample.txt"

    # Initialize an empty list for pages
    pages = []


    # Load PDF
    if os.path.exists(pdf_path):
        loader = PyPDFLoader(pdf_path)
        pages.extend(loader.load())

    # Load TXT
    if os.path.exists(txt_path):
         txt_text = TextLoader(txt_path)
         pages.extend(txt_text.load())

    # Load DOCX
    if os.path.exists(docx_path):
        docx_text = Docx2txtLoader(docx_path)
        pages.extend(docx_text.load())

    if not pages:
        print("No valid files found.")
        return

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