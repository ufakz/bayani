import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL = "gpt-4o-mini"
    TEMPERATURE = 0.7
    
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    APP_TITLE = "Enhanced PDF Chat"
    APP_ICON = ":books:"
    
    CHAT_LOGS_DIR = "chat_logs"
    ALLOWED_EXTENSIONS = ['pdf']
    
    SUPPORTED_LANGUAGES = {
        "English": "en",
        "Hausa": "ha"
    }
    
    DEFAULT_LANGUAGE = "en"
    
    LAYOUT = "wide"