import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, APIError

load_dotenv()

sys.stdin.reconfigure(errors="replace")
def sanitize(s: str) -> str:
    """把任何残留的 surrogate 字符还原或替换掉，保证能被 UTF-8 编码"""
    return s.encode("utf-8", "surrogateescape").decode("utf-8", "replace")
def chat_stream():
    try:
        client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=os.getenv("DEEPSEEK_BASE_URL"))
        history = [{"role": "system", "content": "You are a helpful assistant."}]
        usage_info = 0
        while True:
            user_input = input("you: ").strip()
            if user_input == "exit":
                break
            elif user_input == "clear": 
                history = [{"role": "system", "content": "You are a helpful assistant."}]
                continue
            elif user_input == "":
                continue
            elif user_input == "tokens":
                print(f"Usage: {usage_info} tokens")
                continue
            history.append({"role": "user", "content": sanitize(user_input)})
            
            
           
            try: 
                stream = client.chat.completions.create(model="deepseek-chat", messages=history, stream=True,stream_options= {"include_usage": True})
                collected = ""
                for chunk in stream: 
                    delta = chunk.choices[0].delta.content
                    if delta is not None: 
                        print(delta, end="", flush=True)
                        collected += delta 
                    if chunk.usage is not None:
                        usage_info += chunk.usage.total_tokens
            except KeyboardInterrupt:        
                print("Stream interrupted by user.")
                history.pop()
                continue
            except APIError as e:
                print(f"API Error: {e}")
                history.pop()
                continue                

            history.append({"role": "assistant", "content": sanitize(collected)})
            print("\n")
            
    except KeyboardInterrupt:
        print("Chat session ended.")
if __name__ == "__main__":
    
    chat_stream()