
#实现一个deepseek大模型调用函数
import requests
import json

from backend.config import getConfig

def handler_factory():
    def handler(query: str):
        try:
            url = getConfig()["LLM"]["URL"]

            headers={
                "Authorization": f"Bearer {getConfig()['LLM']['API_KEY']}",
                "Content-Type": "application/json"
            }
            # print(f"query: {query}")
            data={
                "model":getConfig()["LLM"]["MODEL_NAME"],
                "messages":[{"role":"user","content":query}],
                "stream":True
            }
            # 使用stream=True参数确保流式响应
            response=requests.post(
                url,
                headers=headers,
                json=data,
                stream=True
            )
            if response.status_code != 200:
                print(f"[DeepSeek Error] {response.status_code} {response.text}")
                return f"[DeepSeek Error] {response.status_code} {response.text}"
            for line in response.iter_lines():
                # print(line.decode("utf-8"))
                if line and line.startswith(b"data: "):
                    if line[len(b"data: "):].startswith(b"["):
                        return {"message":{"content":""}}
                    chunk_data = json.loads(line[len(b"data: "):].decode("utf-8"))
                    if chunk_data["choices"][0]["finish_reason"]=="Stop":
                        return {"message":{"content":""}}
                    message = chunk_data["choices"][0]["delta"]["content"]
                    # print(f"message: {message}")
                    yield message
        except Exception as e:
            print(f"[OpenAI Error] {str(e)}")
            yield f"[OpenAI Error] {str(e)}"

    return handler

if __name__ == "__main__":
    handler = handler_factory()
    for chunk in handler("Hello, how are you?"):
        print(chunk)