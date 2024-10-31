import streamlit as st
from langchain.callbacks import get_openai_callback
from config.settings import Settings
from core.processor import DocumentProcessor
from core.manager import ConversationManager
from utils import ChatUtils, FileUtils
from templates.html_template import css, bot_template, user_template

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
            with st.expander("View Sources"):
                for doc in response['source_documents']:
                    st.markdown(f"**Source:** {doc.metadata.get('source', 'Unknown')}")
                    st.markdown(f"**Page:** {doc.metadata.get('page', 'Unknown')}")
                    st.markdown("**Relevant Text:**")
                    st.markdown(doc.page_content)
        
        for i, message in enumerate(reversed(st.session_state.chat_history)):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    settings = Settings()
    
    st.set_page_config(
        page_title=settings.APP_TITLE,
        page_icon=settings.APP_ICON,
        layout=settings.LAYOUT
    )
    
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "document_processor" not in st.session_state:
        st.session_state.document_processor = DocumentProcessor()
    
    st.header(settings.APP_TITLE)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_question = st.text_input("Ask a question about your documents")
        if user_question:
            if st.session_state.conversation is None:
                st.warning("Please upload and process documents first!")
            else:
                handle_user_input(user_question)
        
        if hasattr(st.session_state, 'total_tokens'):
            with st.expander("View Usage Metrics"):
                scol1, scol2, scol3, scol4 = st.columns(4)
                scol1.metric("Total Tokens", st.session_state.total_tokens)
                scol2.metric("Prompt Tokens", st.session_state.prompt_tokens)
                scol3.metric("Completion Tokens", st.session_state.completion_tokens)
                scol4.metric("Total Cost ($)", f"{st.session_state.total_cost:.4f}")
    
    with col2:
        st.subheader("Document Management")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here",
            accept_multiple_files=True,
            type=settings.ALLOWED_EXTENSIONS
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Process Documents"):
                if pdf_docs and all(FileUtils.validate_file(pdf, settings.ALLOWED_EXTENSIONS) for pdf in pdf_docs):
                    with st.spinner("Processing documents..."):
                        raw_text = st.session_state.document_processor.get_pdf_text(pdf_docs)
                        text_chunks = st.session_state.document_processor.get_text_chunks(raw_text)
                        vector_store = st.session_state.document_processor.get_vector_store(text_chunks)
                        
                        conversation_manager = ConversationManager()
                        st.session_state.conversation = conversation_manager.create_conversation_chain(vector_store)
                        
                        st.success("Documents processed successfully!")
                        
                        with st.expander("Document Information"):
                            for doc_name, meta in st.session_state.document_processor.metadata.items():
                                st.markdown(f"**{doc_name}**")
                                st.markdown(f"- Title: {meta['title']}")
                                st.markdown(f"- Author: {meta['author']}")
                                st.markdown(f"- Pages: {meta['pages']}")
                else:
                    st.warning("Please upload valid documents first!")
        
        with col2:
            if st.button("Save Chat"):
                if st.session_state.chat_history:
                    saved_file = ChatUtils.save_chat_history(st.session_state.chat_history)
                    st.success(f"Chat history saved to {saved_file}")
                else:
                    st.warning("No chat history to save!")
        
        if st.button("Clear Conversation"):
            st.session_state.conversation = None
            st.session_state.chat_history = None
            st.success("Conversation cleared!")

if __name__ == '__main__':
    main()