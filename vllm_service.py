from vllm import LLM, SamplingParams

class VLLMService:
    def __init__(self, model_name):
        self.llm = LLM(model_name)
        self.sampling_params = SamplingParams(temperature=0.7, top_p=0.95)

    def generate(self, prompt):
        outputs = self.llm.generate([prompt], self.sampling_params)
        return outputs[0].outputs[0].text

    def get_langchain_llm(self):
        from langchain.llms import VLLM
        return VLLM(model=self.llm)
