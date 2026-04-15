import os
from dotenv import load_dotenv

load_dotenv()

# App Settings
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-tutor-key")
DEBUG = True

# Database Settings (Persistent Memory)
# Default to local SQLite for immediate testing without external PostgreSQL setup
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'knowledge_vault.db')}")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Background Tasks (Asynchronous Processing)
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Vector DB Settings
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")

# External APIs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
