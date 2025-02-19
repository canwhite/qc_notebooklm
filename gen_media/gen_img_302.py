import http.client
import json
import requests
import aiohttp
import asyncio
import aiofiles
import os
from dotenv import load_dotenv
load_dotenv()


token = os.getenv("302_TOKEN")


# 正常我生成的是1024，1024的图，但是这里可以生成一张1336*752的图
async def generate_image_async(prompt, filepath, width=1024, height=1024, format="jpeg"):
    url = "https://api.302.ai/302/submit/sdxl-lightning-v2"
    payload = json.dumps({
        "prompt": prompt,
        "image_size": {
            "width": width,
            "height": height
        },
        "embeddings": [],
        "format": format
    })
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
    }
    
    timeout = aiohttp.ClientTimeout(total=15)  # 10* 60 10 minutes timeout
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, headers=headers, data=payload) as response:
            try:
                response_data = await response.json()
                # 如果请求结果有内容
                if 'images' in response_data and len(response_data['images']) > 0:
                    image_url = response_data['images'][0]['url']
                    content_type = response_data['images'][0].get('content_type', 'image/jpeg')
                    
                    file_extension = content_type.split('/')[-1]
                    if file_extension == 'jpeg':
                        file_extension = 'jpg'
                    # os.makedirs('images_folder', exist_ok=True)
                    filename = f'{filepath}'
                    
                    async with session.get(image_url) as image_response:
                        # 这里的status是aiohttp自己封装的吗
                        # 是的，aiohttp在处理HTTP请求时会封装响应对象，其中包括status属性，表示HTTP响应的状态码。
                        # 你可以通过response.status来获取状态码。
                        if image_response.status == 200:
                            content = await image_response.read()
                            async with aiofiles.open(filename, 'wb') as f:
                                await f.write(content)
                            print(f"Image saved as {filename}")
                        else:
                            print(f"Failed to retrieve the image. Status code: {image_response.status}")
                else:
                    print("No images returned in the response data.")
            except Exception as e:
                print(f"An error occurred: {e}")



if __name__ == "__main__":
    # 生成一个podcast封面图，左侧是一个中年男性角色，右侧是一个温婉女性，两人面孔相对，正在对话
    asyncio.run(generate_image_async(
        "Generate a podcast cover picture, on the left is a handsome middle-aged male character, on the right is a gentle and beautiful young woman, the two faces are opposite, are talking, the picture can have podcast words",
        "image.jpg",
        1336,
        752
    ))


