import sqlalchemy

class DatabaseConnector:
    def __init__(self, uri):
        self.uri = uri
        self.engine = None

    def connect(self):
        try:
            self.engine = sqlalchemy.create_engine(self.uri)
            # Test the connection
            with self.engine.connect() as conn:
                conn.execute(sqlalchemy.text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False

    def execute_query(self, query):
        with self.engine.connect() as conn:
            result = conn.execute(sqlalchemy.text(query))
            return result.fetchall()

    def get_table_names(self):
        return sqlalchemy.inspect(self.engine).get_table_names()

    def get_table_schema(self, table_name):
        inspector = sqlalchemy.inspect(self.engine)
        return inspector.get_columns(table_name)
