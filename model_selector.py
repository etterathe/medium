import streamlit as st
from huggingface_hub import HfApi

class ModelSelector:
    def __init__(self):
        self.api = HfApi()

    def get_models(self, task):
        models = self.api.list_models(filter=task, sort="downloads", direction=-1, limit=1000)
        return [model.id for model in models]

    def select_llm_model(self):
        st.subheader("Select LLM Model")
        llm_models = self.get_models("text-generation")
        selected_llm = st.selectbox("Choose an LLM model:", llm_models)
        return selected_llm

    def select_embedding_model(self):
        st.subheader("Select Embedding Model")
        embedding_models = self.get_models("feature-extraction")
        selected_embedding = st.selectbox("Choose an embedding model:", embedding_models)
        return selected_embedding
