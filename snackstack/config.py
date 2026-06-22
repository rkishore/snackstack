"""
Configuration module for the snackstack application.

All modules import this so avoid circular imports.
"""
import os
import sys

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from openai import OpenAI

from snackstack.logger import get_logger

logger = get_logger(__name__)

load_dotenv()

# ----- Validate API key -------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY or OPENAI_API_KEY.startswith("sk-your"):
    logger.error("OPENAI_API_KEY is missing. Copy .env.example → .env and add your key.")
    sys.exit(1)

# ---- Client configuration ------
openai_client = OpenAI(api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

logger.info("OpenAI clients initialised  (model: gpt-4o, embeddings: text-embedding-3-small)")


