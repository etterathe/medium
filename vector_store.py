import torch
import lancedb
import pyarrow as pa
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, embedding_model):
        self.db = lancedb.connect("./lancedb")
        self.schema = pa.schema([
            pa.field("vector", pa.float32(), 384),
            pa.field("text", pa.string()),
        ])
        self.table = self.db.create_table("embeddings", schema=self.schema, mode="overwrite")
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = get_registry().get("sentence-transformers").create(name=embedding_model, device=self.device)

    def add_texts(self, texts):
        """
        Adds a list of texts and their corresponding embeddings to the database.

        Args:
            texts (list): A list of strings to be added.
        """
        embeddings = self.model.encode(texts)
        data = [{"vector": embedding, "text": text} for embedding, text in zip(embeddings, texts)]
        self.table.add(data)

    def similarity_search(self, query, k=5):
        """
        Performs a similarity search on the database and returns the most similar texts.

        Args:
            query (str): The query string to search for.
            k (int): The number of top results to return. Defaults to 5.

        Returns:
            list: A list of strings that are the most similar to the query.
        """
        query_embedding = self.model.encode([query])[0]
        results = self.table.search(query_embedding).limit(k).to_list()
        return [result["text"] for result in results]
