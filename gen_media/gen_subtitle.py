from pathlib import Path
import asyncio
from datetime import timedelta
import srt
from faster_whisper import WhisperModel

# 初始化模型
model = WhisperModel("base", device="cpu", compute_type="float32")

async def generate_subtitle(audioPath,subtilte_path):
    # 转录音频文件
    segments, info = model.transcribe(
        str(audioPath),
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500)
    )

    # 创建SRT字幕
    subtitles = []
    for segment in segments:
        print(f"Transcript: {segment.text}")
        start = timedelta(seconds=segment.start)
        end = timedelta(seconds=segment.end)
        content = segment.text.strip()
        subtitles.append(
            srt.Subtitle(
                index=len(subtitles) + 1,
                start=start,
                end=end,
                content=content
            )
        )

    # 将字幕转换为SRT格式的字符串
    srt_data = srt.compose(subtitles)
    # 保存为SRT文件
    with open(str(subtilte_path), "w", encoding="utf-8") as srt_file:
        srt_file.write(srt_data)

    print("SRT字幕文件已生成：out.srt")

if __name__ == "__main__":
    audio_target_path = Path(__file__).parent.parent / "assets/audios/total_audio.mp3"
    subtilte_path = Path(__file__).parent.parent / "assets/subtitles/out.srt"
    
    asyncio.run(gen_subtitle(audio_target_path,subtilte_path))
