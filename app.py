import streamlit as st
from database_connector import DatabaseConnector
from model_selector import ModelSelector
from vector_store import VectorStore
from langchain_orchestrator import LangChainOrchestrator
from llm_service import LLMService
from chat_interface import ChatInterface

class ChatWithDatabaseApp:
    def __init__(self):
        self.db_connector = None
        self.model_selector = ModelSelector()
        self.vector_store = None
        self.orchestrator = None
        self.llm_service = None

    def initialize_chat_system(self, llm_model, embedding_model):
        """Initializes the chat system components only if the button is pressed."""
        if st.sidebar.button("Initialize Chat System"):
            if self.db_connector:
                st.session_state.llm_service = LLMService(llm_model)
                st.session_state.vector_store = VectorStore(embedding_model)
                st.session_state.orchestrator = LangChainOrchestrator(
                    st.session_state.llm_service.generator,
                    self.db_connector,
                    st.session_state.vector_store
                )
                st.session_state.chat_ui = ChatInterface(st.session_state.orchestrator.invoke_chain)
                st.success("Chat system initialized successfully!")
            else:
                st.error("Please connect to a database first.")

    def run_chat_ui(self):
        """Run the chat UI if it has been initialized."""
        if "chat_ui" in st.session_state:
            st.session_state.chat_ui.run()
            st.sidebar.markdown("---")
            st.sidebar.button('Clear Chat History', on_click=st.session_state.chat_ui.clear_chat_history)
        else:
            st.warning("Chat system not initialized. Please initialize first.")


    def run(self):
        st.set_page_config(page_title="🔮 medium")
        with st.sidebar:
            st.markdown("""
                # 🔮 medium
                Chat with your SQL databases and discover world of new insights

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
            llm_model = self.model_selector.select_llm_model()
            embedding_model = self.model_selector.select_embedding_model()

        # Initialize components
        self.initialize_chat_system(llm_model, embedding_model)

        # Interface
        self.run_chat_ui()


if __name__ == "__main__":
    app = ChatWithDatabaseApp()
    app.run()
