import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.environ

SERVER_BASE_URL = ENV.get("SERVER_BASE_URL")
CLIENT_BASE_URL = ENV.get("CLIENT_BASE_URL")
GOOGLE_API_KEY = ENV.get("GOOGLE_API_KEY")


if not SERVER_BASE_URL:
    raise Exception("SERVER_BASE_URL is not set")
if not CLIENT_BASE_URL:
    raise Exception("CLIENT_BASE_URL is not set")
if not GOOGLE_API_KEY:
    raise Exception("GOOGLE_API_KEY is not set")
