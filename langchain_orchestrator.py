from langchain.schema import Document
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

class LangChainOrchestrator:
    def __init__(self, db_connector, vector_store):
        self.db_connector = db_connector
        self.vector_store = vector_store
        self.sql_database = SQLDatabase(db_connector.engine)
        self.sql_chain = None

    def initialize_chain(self, llm):
        self.sql_chain = SQLDatabaseChain.from_llm(llm, self.sql_database, verbose=True)

    def add_schema_to_vector_store(self):
        schema = self.sql_database.get_table_info()
        self.vector_store.add_texts([schema])

    def query(self, user_input):
        relevant_docs = self.vector_store.similarity_search(user_input)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        full_query = f"Context: {context}\nQuestion: {user_input}"
        return self.sql_chain.run(full_query)
