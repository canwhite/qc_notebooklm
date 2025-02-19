# 生成图片
import requests
from PIL import Image
import io
import os
from dotenv import load_dotenv
import aiohttp
import asyncio
import time

load_dotenv()
hf_token = os.getenv("HF_TOKEN")
#角色，任务， 背景， 要求， 输出格式， 限制条件， 示例


def rate_limit(max_calls, period):
    def decorator(func):
        calls = []
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [call for call in calls if call > now - period]
            if len(calls) >= max_calls:
                time_to_wait = period - (now - calls[0])
                print(f"Rate limit reached. Waiting for {time_to_wait:.2f} seconds.")
                time.sleep(time_to_wait)
                calls.clear()
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

    
@rate_limit(max_calls=1, period=10)  # 每10秒最多1次请求
async def generate_image(prompt, output_file="image3.png"):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    
    if hf_token is None:
        raise ValueError("HF_TOKEN is not set in the environment variables.")

    headers = {"Authorization": f"Bearer {hf_token}"}
    headers["Content-Type"] = "application/json"
    payload = {
        "inputs": prompt,
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(API_URL, headers=headers, json=payload) as response:
                if response.status == 200:
                    image_bytes = await response.read()
                    image = Image.open(io.BytesIO(image_bytes))
                    image.save(output_file)
                else:
                    print(f"Error: Received status code {response.status}")
        except aiohttp.ClientConnectorError as e:
            print(f"Connection error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    target = f""" 
    Klein and Azik face off inside a house. Klein wields a longsword while Azik holds a spear. 
    They stand in a tense standoff, their weapons pointed at each other. 
    The tip of Klein's sword meets Azik's spearhead, their blades crossing with a metallic touch. 
    Both warriors raise their weapons, ready for combat.
    """
    # 示例用法
    asyncio.run(generate_image(target))






