from langchain.llms import HuggingFacePipeline


class LLMService:
    def __init__(self, model_name):
        self.generator = HuggingFacePipeline.from_model_id(
            model_id=model_name,
            task="text-generation",
            pipeline_kwargs={"max_new_tokens": 600},
        )
