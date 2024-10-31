from typing import Dict, Any

class LanguageConfig:
    TEMPLATES: Dict[str, Dict[str, Any]] = {
        "en": {
            "system_message": """
            Context: {context}
            
            Chat History: {chat_history}
            
            Question: {question}
            
            Answer: Let's think about this step by step:""",
            "ui": {
                "ask_question": "Ask a question about your documents",
                "upload_prompt": "Upload your PDFs here",
                "process_docs": "Process Documents",
                "processing_msg": "Processing documents...",
                "success_msg": "Documents processed successfully!",
                "upload_warning": "Please upload valid documents first!",
                "save_chat": "Save Chat",
                "chat_saved": "Chat history saved to {file}",
                "no_chat": "No chat history to save!",
                "clear_chat": "Clear Conversation",
                "cleared_msg": "Conversation cleared!",
                "upload_first": "Please upload and process documents first!",
                "view_metrics": "View Usage Metrics",
                "view_sources": "View Sources",
                "doc_management": "Document Management",
                "doc_info": "Document Information",
                "metadata": {
                    "title": "Title",
                    "author": "Author",
                    "pages": "Pages"
                }
            }
        },
        "ha": {
            "system_message": """
            System: Ku amsa duk tambayoyin a harshen Hausa. Yi amfani da bayanan da aka baku a cikin takarda don bayar da amsa mai ma'ana kuma cikakke.

            Context: {context}
            
            Chat History: {chat_history}
            
            Question: {question}
            
            Answer: Let's think about this step by step in Hausa:""",
            "ui": {
                "ask_question": "Yi tambaya game da takardunku",
                "upload_prompt": "Ɗora fayilolin PDF a nan",
                "process_docs": "Aiwatar da Takardu",
                "processing_msg": "Ana aiwatar da takardu...",
                "success_msg": "An yi nasarar aiwatar da takardu!",
                "upload_warning": "Da fatan za a fara ɗora ingantattun takardu!",
                "save_chat": "Ajiye Tattaunawa",
                "chat_saved": "An ajiye tarihin tattaunawa a {file}",
                "no_chat": "Babu tarihin tattaunawa da za a ajiye!",
                "clear_chat": "Share Tattaunawa",
                "cleared_msg": "An share tattaunawa!",
                "upload_first": "Da fatan za a fara ɗora takardu sannan a yi aiki da su!",
                "view_metrics": "Duba Ƙididdigar Amfani",
                "view_sources": "Duba Tushen Bayani",
                "doc_management": "Gudanar da Takardu",
                "doc_info": "Bayanan Takarda",
                "metadata": {
                    "title": "Take",
                    "author": "Marubuci",
                    "pages": "Shafuku"
                }
            }
        }
    }

    @classmethod
    def get_prompt_template(cls, language: str) -> str:
        return cls.TEMPLATES[language]["system_message"]

    @classmethod
    def get_ui_text(cls, language: str, key: str, **kwargs) -> str:
        text = cls.TEMPLATES[language]["ui"]
        for k in key.split('.'):
            text = text[k]
        return text.format(**kwargs) if kwargs else text