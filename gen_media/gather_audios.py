import asyncio
import subprocess
from pathlib import Path
import asyncio


# TODO: 如果音频类型是一致的，可以使用这个去合并音频
async def merge_audios_old(audio_paths, output_path):
    # 将所有输入文件转换为字符串
    inputs = []
    for path in audio_paths:
        inputs.extend(["-i", str(path)])
    
    command = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex",
        "concat=n=" + str(len(audio_paths)) + ":v=0:a=1",
        str(output_path)
    ]
    
    # 执行命令
    subprocess.run(command, check=True)



async def merge_audios(audio_paths, output_path):
    # 构建输入参数和滤镜
    inputs = []
    filter_parts = []
    
    # 添加所有输入文件
    for path in audio_paths:
        inputs.extend(["-i", str(path)])
    
    # 构建 filter_complex 字符串
    filter_str = ''.join(f'[{i}:a]' for i in range(len(audio_paths))) + \
                f'concat=n={len(audio_paths)}:v=0:a=1[outa]'
    
    command = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_str,
        "-map", "[outa]",
        str(output_path)
    ]
    
    # 执行命令
    subprocess.run(command, check=True)


if __name__ == "__main__":

    audio_paths = [str(Path(__file__).parent.parent / "assets/audios" / "part2_1.wav"),str(Path(__file__).parent.parent / "assets/audios" / "part2_2.wav")]
    asyncio.run(merge_audios(audio_paths,"output_audio.wav"))







