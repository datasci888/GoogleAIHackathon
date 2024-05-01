import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.environ

SERVER_BASE_URL = ENV.get("SERVER_BASE_URL")
CLIENT_BASE_URL = ENV.get("CLIENT_BASE_URL")
GOOGLE_API_KEY = ENV.get("GOOGLE_API_KEY")
PINECONE_API_KEY = ENV.get("PINECONE_API_KEY")
PINECONE_URL = ENV.get("PINECONE_URL")
OPENAI_API_KEY = ENV.get("OPENAI_API_KEY")
NEO4J_USERNAME = ENV.get("NEO4J_USERNAME")
NEO4J_PASSWORD = ENV.get("NEO4J_PASSWORD")
NEO4J_URL = ENV.get("NEO4J_URL")

if not SERVER_BASE_URL:
    raise Exception("SERVER_BASE_URL is not set")
if not CLIENT_BASE_URL:
    raise Exception("CLIENT_BASE_URL is not set")
if not GOOGLE_API_KEY:
    raise Exception("GOOGLE_API_KEY is not set")
if not PINECONE_API_KEY:
    raise Exception("PINECONE_API_KEY is not set")
if not PINECONE_URL:
    raise Exception("PINECONE_URL is not set")
