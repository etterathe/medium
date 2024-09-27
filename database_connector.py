import sqlalchemy

class DatabaseConnector:
    def __init__(self, uri):
        self.uri = uri
        self.engine = sqlalchemy.create_engine(self.uri) if uri != "" else None

    def connect(self):
        """
        Attempt to establish a connection to the database.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(sqlalchemy.text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False

    def execute_query(self, query):
        """
        Execute a SQL query and return the results.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            list: The result of the query as a list of tuples.
        """
        with self.engine.connect() as conn:
            result = conn.execute(sqlalchemy.text(query))
            return result.fetchall()

    def get_table_names(self):
        """
        Retrieve a list of all table names in the database.

        Returns:
            list: A list of table names.
        """
        return sqlalchemy.inspect(self.engine).get_table_names()

    def get_table_schema(self, table_name):
        """
        Retrieve the schema (columns) for a specific table.

        Args:
            table_name (str): The name of the table.

        Returns:
            list: A list of dictionaries describing the columns in the table.
        """
        inspector = sqlalchemy.inspect(self.engine)
        return inspector.get_columns(table_name)

    def get_table_info(self, table_name):
        """
        Retrieve information about a specific table, including its comment.

        Args:
            table_name (str): The name of the table.

        Returns:
            str: The comment associated with the table, or None if no comment is set.
        """
        inspector = sqlalchemy.inspect(self.engine)
        return inspector.get_table_comment(table_name)
