class NLPProcessor:
    def __init__(self, orchestrator, vllm_service):
        self.orchestrator = orchestrator
        self.vllm_service = vllm_service
        self.orchestrator.initialize_chain(self.vllm_service.get_langchain_llm())

    def process_query(self, query):
        try:
            result = self.orchestrator.query(query)
            return result
        except Exception as e:
            return f"An error occurred while processing your query: {str(e)}"
