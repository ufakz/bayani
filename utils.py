import os
import json
from datetime import datetime
from config.settings import Settings

#TODO: Separate the utils into their respective files

# ChatUtils
class ChatUtils:
    @staticmethod
    def save_chat_history(chat_history):
        settings = Settings()
        if not os.path.exists(settings.CHAT_LOGS_DIR):
            os.makedirs(settings.CHAT_LOGS_DIR)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{settings.CHAT_LOGS_DIR}/chat_history_{timestamp}.json"
        
        chat_data = []
        for message in chat_history:
            chat_data.append({
                "role": "user" if isinstance(message, dict) else "assistant",
                "content": message.content if hasattr(message, 'content') else message['content']
            })
        
        with open(filename, 'w') as f:
            json.dump(chat_data, f, indent=2)
        
        return filename

# FileUtils
class FileUtils:
    @staticmethod
    def validate_file(file, allowed_extensions):
        if file is None:
            return False
        return file.name.split('.')[-1].lower() in allowed_extensions