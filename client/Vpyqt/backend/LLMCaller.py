from backend.config import getConfig

class LLMCaller:
    def __init__(self):
        self.model_registry={}
        self.response_generator=None

    def register_model(self,name:str,handler_factory):
        self.model_registry[name] = handler_factory

    def stream(self, query: str):
        handler = self.model_registry[getConfig()["LLM"]["PROVIDER"]]()  # 动态注入 model, api_key, base_url
        self.response_generator = handler(query)
        if self.response_generator is None:
            return
        try:
            while True:
                yield next(self.response_generator)
        except StopIteration:
            return
        
if __name__ == "__main__":
    llm_caller = LLMCaller()
    from backend.provider import deepseek
    llm_caller.register_model("deepseek", deepseek.handler_factory)
    # Example usage
    for response in llm_caller.stream("Hello, how are you?"):
        print(response)