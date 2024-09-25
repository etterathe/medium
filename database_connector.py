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

    def is_connected(self):
        return self.engine is not None

    def execute_query(self, query):
        if not self.is_connected():
            raise Exception("Not connected to a database")

        with self.engine.connect() as conn:
            result = conn.execute(sqlalchemy.text(query))
            return result.fetchall()

    def get_table_names(self):
        if not self.is_connected():
            raise Exception("Not connected to a database")

        return sqlalchemy.inspect(self.engine).get_table_names()

    def get_table_schema(self, table_name):
        if not self.is_connected():
            raise Exception("Not connected to a database")

        inspector = sqlalchemy.inspect(self.engine)
        return inspector.get_columns(table_name)
