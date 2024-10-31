from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from config.settings import Settings
from config.language import LanguageConfig

class ConversationManager:
    def __init__(self, language="en"):
        self.settings = Settings()
        self.language = language
        
    def get_prompt_template(self):
        template = LanguageConfig.get_prompt_template(self.language)
        return PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template=template
        )
    
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
        
        qa_prompt = self.get_prompt_template()
        
        return ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
            memory=memory,
            return_source_documents=True,
            get_chat_history=lambda h: h,
            combine_docs_chain_kwargs={'prompt': qa_prompt}
        )