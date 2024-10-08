import os
import re
from pinecone import Pinecone, ServerlessSpec
from preprocess_doc import get_docs
import openai
from openai import OpenAI

import dotenv


dotenv.load_dotenv()

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()
MODEL = "text-embedding-3-large"
namespace = os.getenv('PINECONE_NAMESPACE')

pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index_name = os.getenv('PINECONE_INDEX')

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=2,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-east-1'
        ) 
   ) 

index = pc.Index(index_name)


# Define a function to preprocess text
def preprocess_text(text):
    # Replace consecutive spaces, newlines and tabs
    text = re.sub(r'\s+', ' ', text)
    return text

# Define a function to create embeddings
def create_embeddings(texts):
    num_vectors = get_number_vectors_in_namespace()
    for i, text in enumerate(texts[num_vectors:]):
        i += num_vectors
        print(f"Disease: {i+1}")
        embedding = client.embeddings.create(input = [text], model=MODEL).data[0].embedding

        upsert_embeddings_to_pinecone(index, embedding, i, text)

# Define a function to upsert embeddings to Pinecone
def upsert_embeddings_to_pinecone(index, embedding, id, page_content):
    index.upsert(vectors=[
        {"id": str(id), "values": embedding, "metadata": {"page_content": page_content}}
    ], namespace=namespace)

def get_number_vectors_in_namespace():
    try:
        num_vectors = 0
        all_ids = []
        for ids in index.list(namespace=namespace):
            all_ids = all_ids + ids

        num_vectors = len(all_ids)

        print(f"Number of uploaded vectors: {num_vectors}")
        return num_vectors
    except Exception as e:
        print(f"Error: {e}")


print("Reading PDF")
file_path = "disease_book.pdf"
texts = get_docs()

print("Creating Embeddings")
create_embeddings(texts)
