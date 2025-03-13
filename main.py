import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback
from config.settings import Settings
from config.language import LanguageConfig
from core.processor import DocumentProcessor
from core.manager import ConversationManager
from utils import ChatUtils, FileUtils
from templates.html_template import css, bot_template, user_template

def initialize_session_state():
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "document_processor" not in st.session_state:
        st.session_state.document_processor = DocumentProcessor()
    if "language" not in st.session_state:
        st.session_state.language = Settings.DEFAULT_LANGUAGE

def handle_user_input(user_question):
    with get_openai_callback() as cb:
        response = st.session_state.conversation({
            'question': user_question
        })
        
        
        st.session_state.chat_history = response['chat_history']
        st.session_state.total_tokens = cb.total_tokens
        st.session_state.prompt_tokens = cb.prompt_tokens
        st.session_state.completion_tokens = cb.completion_tokens
        st.session_state.total_cost = cb.total_cost
        
        if 'source_documents' in response:
            with st.expander(LanguageConfig.get_ui_text(st.session_state.language, "view_sources")):
                for doc in response['source_documents']:
                    st.markdown(f"**Source:** {doc.metadata.get('source', 'Unknown')}")
                    st.markdown(f"**Page:** {doc.metadata.get('page', 'Unknown')}")
                    st.markdown(f"**{LanguageConfig.get_ui_text(st.session_state.language, 'view_sources')}:**")
                    st.markdown(doc.page_content)
        
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        
        

def main():
    settings = Settings()
    initialize_session_state()
    
    st.set_page_config(
        page_title=settings.APP_TITLE,
        page_icon=settings.APP_ICON,
        layout=settings.LAYOUT
    )
    
    st.write(css, unsafe_allow_html=True)
    
    # Sidebar content
    with st.sidebar:
        selected_language = st.selectbox(
            "Select Language / Zaɓi Harshe",
            options=list(settings.SUPPORTED_LANGUAGES.keys()),
            index=0 if st.session_state.language == "en" else 1
        )
        
        new_language = settings.SUPPORTED_LANGUAGES[selected_language]
        if new_language != st.session_state.language:
            st.session_state.language = new_language
            st.session_state.conversation = None
            st.session_state.chat_history = None
            st.rerun()
        
        st.divider()  
        
        st.subheader(LanguageConfig.get_ui_text(st.session_state.language, "doc_management"))
        
        pdf_docs = st.file_uploader(
            LanguageConfig.get_ui_text(st.session_state.language, "upload_prompt"),
            accept_multiple_files=True,
            type=settings.ALLOWED_EXTENSIONS
        )
        
        if st.button(LanguageConfig.get_ui_text(st.session_state.language, "process_docs")):
            if pdf_docs and all(FileUtils.validate_file(pdf, settings.ALLOWED_EXTENSIONS) for pdf in pdf_docs):
                with st.spinner(LanguageConfig.get_ui_text(st.session_state.language, "processing_msg")):
                    raw_text = st.session_state.document_processor.get_pdf_text(pdf_docs)
                    text_chunks = st.session_state.document_processor.get_text_chunks(raw_text)
                    vector_store = st.session_state.document_processor.get_vector_store(text_chunks)
                    
                    conversation_manager = ConversationManager(language=st.session_state.language)
                    st.session_state.conversation = conversation_manager.create_conversation_chain(vector_store)
                    
                    st.success(LanguageConfig.get_ui_text(st.session_state.language, "success_msg"))
                    
                    with st.expander(LanguageConfig.get_ui_text(st.session_state.language, "doc_info")):
                        for doc_name, meta in st.session_state.document_processor.metadata.items():
                            st.markdown(f"**{doc_name}**")
                            st.markdown(f"- {LanguageConfig.get_ui_text(st.session_state.language, 'metadata.title')}: {meta['title']}")
                            st.markdown(f"- {LanguageConfig.get_ui_text(st.session_state.language, 'metadata.author')}: {meta['author']}")
                            st.markdown(f"- {LanguageConfig.get_ui_text(st.session_state.language, 'metadata.pages')}: {meta['pages']}")
            else:
                st.warning(LanguageConfig.get_ui_text(st.session_state.language, "upload_warning"))
    
    # Main content area
    st.header(f"Bayani {settings.APP_ICON}")
    
    # Create a container for chat history with fixed height and scrolling
    chat_container = st.container()
    
    # Create a container for the input box at the bottom
    input_container = st.container()
    
    # Place the input box at the bottom
    with input_container:
        user_question = st.text_input(
            LanguageConfig.get_ui_text(st.session_state.language, "ask_question"),
            key="user_input"
        )
    
    # Display chat history in scrollable container
    with chat_container:
        if user_question:
            if st.session_state.conversation is None:
                st.warning(LanguageConfig.get_ui_text(st.session_state.language, "upload_first"))
            else:
                handle_user_input(user_question)

if __name__ == '__main__':
    main()