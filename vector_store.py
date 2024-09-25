import lancedb
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, embedding_model):
        self.db = lancedb.connect("./lancedb")
        self.table = self.db.create_table("embeddings", schema={"vector": "float32[384]", "text": "string"})
        self.model = SentenceTransformer(embedding_model)

    def add_texts(self, texts):
        embeddings = self.model.encode(texts)
        data = [{"vector": embedding, "text": text} for embedding, text in zip(embeddings, texts)]
        self.table.add(data)

    def similarity_search(self, query, k=5):
        query_embedding = self.model.encode([query])[0]
        results = self.table.search(query_embedding).limit(k).to_list()
        return [result["text"] for result in results]
