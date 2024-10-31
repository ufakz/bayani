from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from config.settings import Settings

class ConversationManager:
    def __init__(self):
        self.settings = Settings()
    
    def create_conversation_chain(self, vector_store):
        llm = ChatOpenAI(
            model=self.settings.DEFAULT_MODEL,
            temperature=self.settings.TEMPERATURE,
            streaming=True
        )
        
        memory = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=True,
            output_key='answer'
        )
        
        return ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
            memory=memory,
            return_source_documents=True,
            get_chat_history=lambda h: h
        )