import streamlit as st
from database_connector import DatabaseConnector
from model_selector import ModelSelector
from vector_store import VectorStore
from langchain_orchestrator import LangChainOrchestrator
from vllm_service import VLLMService
from nlp_processor import NLPProcessor

class ChatWithDatabaseApp:
    def __init__(self):
        self.db_connector = None
        self.model_selector = ModelSelector()
        self.vector_store = None
        self.orchestrator = None
        self.vllm_service = None
        self.nlp_processor = None

    def run(self):
        st.markdown("""
            # :crystal_ball: medium
            #### Chat with your SQL databases and discover world of new insights

            ---
            """)

        # Database Connection
        st.subheader("Database Connection")
        db_uri = st.text_input("Enter your database URI:", placeholder="postgresql://username:password@host:port/database_name")
        self.db_connector = DatabaseConnector(db_uri)
        if st.button("Connect to Database"):
            if self.db_connector.connect():
                st.success("Connected to database successfully!")
            else:
                st.error("Failed to connect to database. Please check your URI.")

        # Model Selection
        print(self.db_connector)
        llm_model = self.model_selector.select_llm_model()
        embedding_model = self.model_selector.select_embedding_model()

        # Initialize components
        if st.button("Initialize Chat System"):
            if self.db_connector:
                self.vector_store = VectorStore(embedding_model)
                self.orchestrator = LangChainOrchestrator(self.db_connector, self.vector_store)
                self.vllm_service = VLLMService(llm_model)
                self.nlp_processor = NLPProcessor(self.orchestrator, self.vllm_service)
                st.success("Chat system initialized successfully!")
            else:
                st.error("Please connect to a database first.")
        else:
            st.warning("Please initialize the chat system.")

        # Chat Interface
        user_input = st.text_input("Ask a question about your database:")
        if st.button("Send"):
            if self.nlp_processor:
                response = self.nlp_processor.process_query(user_input)
                st.write("Response:", response)
            else:
                st.error("Please initialize the chat system first.")

if __name__ == "__main__":
    app = ChatWithDatabaseApp()
    app.run()
