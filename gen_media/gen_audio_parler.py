import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import logging
import os
from concurrent.futures import ProcessPoolExecutor

# 设置日志级别来减少警告信息
logging.getLogger("transformers").setLevel(logging.ERROR)

torch.manual_seed(42)  # 设置随机种子

def generate_audio_with_parler(text_prompt, description, output_file):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load model and tokenizer
    model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler-tts-mini-v1").to(device)
    tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")

    # Tokenize inputs
    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(text_prompt, return_tensors="pt").input_ids.to(device)

    # Generate audio
    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()

    # 检查文件是否存在，如果存在则删除
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"文件 {output_file} 已存在，已删除。")

    sf.write(output_file, audio_arr, model.config.sampling_rate)


if __name__ == "__main__":

    # Define text and description
    text_prompt = """
    Exactly! And the distillation part is where you take a LARGE-model,and compress-it down into a smaller, more efficient model that can run on devices with limited resources.
    """
    female_prompt = """
    Laura's voice is expressive and dramatic in delivery, 
    speaking at a slow pace with a very close recording that almost has no background noise.
    """
    male_prompt = """A middle-aged male voice with a deep and playful tone. 
    The voice is warm and friendly, with a slightly faster delivery that conveys humor and wit. 
    The speaker has a rich and resonant voice, with a natural and conversational style.
     The audio is clear and close, with minimal background noise, and the microphone is positioned very close to the speaker's mouth."""


    output_file = "output_male.wav"

    #然后以多进程的方式调用这些方法
    with ProcessPoolExecutor(max_workers = os.cpu_count()) as executor:
        executor.map(generate_audio_with_parler, [text_prompt], [male_prompt], [output_file])




