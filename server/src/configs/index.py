import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.environ


GEMINI_API_KEY = ENV.get("GEMINI_API_KEY")
SERVER_BASE_URL = ENV.get("SERVER_BASE_URL")
CLIENT_BASE_URL = ENV.get("CLIENT_BASE_URL")