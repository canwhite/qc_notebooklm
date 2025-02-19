from transformers import pipeline
from datasets import load_dataset
import soundfile as sf
import torch
import asyncio
import subprocess
from transformers import AutoTokenizer
import os
#注意Flase和True用大写
async def generate_audio(text, output_file, is_chunk=False):
    synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts", device="cpu")
    embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
    speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
    max_token = synthesiser.tokenizer.model_max_length

    # 如果是分块处理，直接生成音频
    if is_chunk:
        speech = synthesiser(
            text,
            forward_params={"speaker_embeddings": speaker_embedding}
        )
        sf.write(output_file, speech["audio"], samplerate=speech["sampling_rate"])
        return

    # 这个计算方法会不会和microsoft/speecht5_tts计算的结果不一致
    # 为了确保计算结果一致，我们可以使用相同的tokenizer来计算token数量
    tokenizer = AutoTokenizer.from_pretrained("microsoft/speecht5_tts")
    tokens = tokenizer.tokenize(text)
    token_count = len(tokens)
    print(f"输入文本的token数量为: {token_count}")


    if token_count > max_token:
        # 按句子分割文本
        sentences = text.split('.')
        current_chunk = ""
        chunks = []
        current_tokens = 0
        #按句循环
        for sentence in sentences:
            sentence = sentence.strip() + "."
            sentence_tokens = len(tokenizer.tokenize(sentence))
            
            if current_tokens + sentence_tokens > max_token:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence
                current_tokens = sentence_tokens
            else:
                current_chunk = current_chunk + " " + sentence if current_chunk else sentence
                current_tokens += sentence_tokens
        
        if current_chunk:
            chunks.append(current_chunk)

        # 临时文件存储路径
        temp_files = []
        
        # 生成每个块的音频
        for i, chunk in enumerate(chunks):
            chunk_output_file = f"temp_chunk_{i+1}.wav"
            temp_files.append(chunk_output_file)
            await generate_audio(chunk, chunk_output_file, is_chunk=True)

        # 准备合并音频文件的命令
        merge_command = ["ffmpeg", "-y"]
        for audio_file in temp_files:
            merge_command.extend(["-i", audio_file])
        
        filter_complex = f"concat=n={len(temp_files)}:v=0:a=1"
        merge_command.extend(["-filter_complex", filter_complex, output_file])

        try:
            subprocess.run(merge_command, check=True)
            print(f"合并后的音频文件已保存为 {output_file}")
            
            # 清理临时文件
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

        except subprocess.CalledProcessError as e:
            print(f"合并音频文件时出错: {e}")
            # 清理临时文件
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

    else:
        speech = synthesiser(
            text,
            forward_params={"speaker_embeddings": speaker_embedding}
        )
        sf.write(output_file, speech["audio"], samplerate=speech["sampling_rate"])

if __name__ == "__main__":
    # 示例用法
    text = """Hello, my dog is cooler than you! 
    I want you to help me deal with this error, but I have not located the specific problem, how can I do this, I feel very troublesome.
    I want you to help me deal with this error, but I have not located the specific problem, how can I do this, I feel very troublesome.
    I want you to help me deal with this error, but I have not located the specific problem, how can I do this, I feel very troublesome.
    I want you to help me deal with this error, but I have not located the specific problem, how can I do this, I feel very troublesome.
    I want you to help me deal with this error, but I have not located the specific problem, how can I do this, I feel very troublesome."""
    asyncio.run(generate_audio(text, "speech.wav"))
