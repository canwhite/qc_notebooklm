from pathlib import Path
import asyncio
import subprocess

async def gen_video_with_subtitles(image_file, audio_file, subtitle_file, video_file):
    # 获取音频时长
    audio_duration_command = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration", 
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_file)
    ]
    audio_duration = subprocess.run(audio_duration_command, stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE, text=True).stdout
    audio_duration = float(audio_duration)
    
    # 计算总帧数（假设25fps）
    fps = 25
    total_frames = int(audio_duration * fps)

    command = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(image_file),
        "-i", str(audio_file),
        "-vf", f"scale=1280:720,zoompan=z='min(zoom+0.0015,1.4)':x='0':y='0':d={total_frames},subtitles={str(subtitle_file)}",
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-shortest",
        str(video_file)
    ]

    subprocess.run(command, check=True)




async def gen_vidio_without_zoom(image_file, audio_file, subtitle_file,video_file):
    command = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(image_file),
        "-i", str(audio_file),
        "-vf", f"subtitles={str(subtitle_file)}:force_style='Fontsize=20'",
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-shortest",
        str(video_file)
    ]
    subprocess.run(command, check=True)



if __name__ == "__main__":

    # 
    target_image_directory = Path(__file__).parent.parent / "assets/images" / "part2_1.jpg"
    target_audio_directory = Path(__file__).parent.parent / "assets/audios" / "part2_1.wav"
    target_subtitle_file = Path(__file__).parent.parent / "assets/subtitles" / "part2_1.srt"
    output_video_path = Path(__file__).parent.parent / "assets/videos" / "output_video_with_subtitles_2_1.mp4"
    
    asyncio.run(gen_video_with_subtitles(target_image_directory, target_audio_directory, 
                                       target_subtitle_file, output_video_path))
