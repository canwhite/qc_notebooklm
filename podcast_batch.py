import sys
import os
from dotenv import load_dotenv
from pdf_handle import get_pdf_content
from prompts import WRITE_PROMPT,REWRITE_PROMPT,MALE_PROMPT,FEMALE_PROMPT
from agents import AgentPool
from pathlib import Path
from gen_media import generate_audio_with_parler,merge_audios,generate_subtitle,gen_vidio_without_zoom
from concurrent.futures import ProcessPoolExecutor
import asyncio

load_dotenv()

pool = AgentPool()


#拿到podcast的生成地址，如果没有自己创建下
target_podcast_dictionary = Path(__file__).parent / "assets" / "podcasts"
target_podcast_result = Path(__file__).parent / "assets/podresult"

audio_output_path =  target_podcast_result.joinpath("output.wav")
subtitle_output_path = target_podcast_result.joinpath("output.srt")

#有一张封面图片
image_output_path = target_podcast_result.joinpath("image.jpg")
video_output_path = target_podcast_result.joinpath("output.mp4")

paf_target_path = os.getenv("PDF_SAVE_PATH")
doc_name = "example"
doc =  paf_target_path +  f"/{doc_name}.pdf"


async def writer_gen(content):
    pool.add_agent("writer_agent",WRITE_PROMPT)
    writer_res = pool.execute_and_release("writer_agent",content)
    return writer_res   


async def rewriter_gen(writer_res):
    pool.add_agent("rewriter_agent",REWRITE_PROMPT)
    rewriter_res = pool.execute_and_release("rewriter_agent",writer_res)
    return rewriter_res


def generate_audio(audio_arr):
    with ProcessPoolExecutor() as executor: 
        # with ProcessPoolExecutor(max_workers = os.cpu_count()) as executor:
        #     executor.map(generate_audio_with_parler, [text_prompt], [male_prompt], [output_file])
        prompts = [item[1] for item in audio_arr]
        descriptions = []
        for speaker, prompt in audio_arr:
            if speaker == "Speaker 1":
                descriptions.append(FEMALE_PROMPT)
            else:
                descriptions.append(MALE_PROMPT)
        
        executor.map(generate_audio_with_parler, prompts, descriptions, [f"{str(target_podcast_dictionary)}/{i+1}.wav" for i in range(len(prompts))])




if __name__ == "__main__":

    # 提取pdf内容
    content = get_pdf_content(doc)
    print(content)

    # 初步改写
    writer_res =  asyncio.run(writer_gen(content))
    print(writer_res)

    # 改成podcast稿
    audio_arr =  asyncio.run(rewriter_gen(writer_res))
    print(audio_arr)

    # 生成音频文件
    generate_audio(audio_arr)

    # 排序
    audio_files = sorted(target_podcast_dictionary.glob("*.wav"), key=lambda x: int(x.stem))

    # 合并音频
    asyncio.run(merge_audios(audio_files,audio_output_path)) 


    # 生成字幕
    asyncio.run(generate_subtitle(str(audio_output_path),str(subtitle_output_path)))

    # 生成视频
    asyncio.run(gen_vidio_without_zoom(str(image_output_path),str(audio_output_path),str(subtitle_output_path),str(video_output_path)))






   





    












































































