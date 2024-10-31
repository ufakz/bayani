from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from config.settings import Settings

class DocumentProcessor:
    def __init__(self):
        self.metadata = {}
        self.settings = Settings()
    
    def get_pdf_text(self, pdf_docs):
        text = ""
        self.metadata = {}
        
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            pdf_info = pdf_reader.metadata
            
            self.metadata[pdf.name] = {
                "title": pdf_info.get("/Title", "Unknown"),
                "author": pdf_info.get("/Author", "Unknown"),
                "creation_date": pdf_info.get("/CreationDate", "Unknown"),
                "pages": len(pdf_reader.pages)
            }
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text += f"\nDocument: {pdf.name} | Page: {page_num}\n"
                text += page.extract_text()
        
        return text

    def get_text_chunks(self, raw_text):
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""],
            chunk_size=self.settings.CHUNK_SIZE,
            chunk_overlap=self.settings.CHUNK_OVERLAP,
            length_function=len
        )
        return text_splitter.split_text(raw_text)

    def get_vector_store(self, text_chunks):
        embeddings = OpenAIEmbeddings()
        return FAISS.from_texts(text_chunks, embedding=embeddings)