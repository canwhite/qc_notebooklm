import asyncio
import subprocess
from pathlib import Path

# 这段代码的主要功能是将多个视频文件合并成一个视频文件。
# 首先，代码导入了必要的模块，包括 `asyncio` 用于异步操作，`subprocess` 用于运行外部命令，`Path` 用于处理文件路径。
# 然后，定义了一个异步函数 `merge_videos`，该函数接受一个视频路径列表 `video_paths` 和一个输出路径 `output_path`。
# 在函数内部，构建了一个 `ffmpeg` 命令，用于将多个视频文件合并成一个视频文件。`ffmpeg` 是一个强大的多媒体处理工具，可以处理视频、音频等多种格式。
# 命令的构建过程如下：
# 1. 使用 `ffmpeg` 命令启动。
# 2. 使用 `-y` 选项表示如果输出文件已经存在，则覆盖它。
# 3. 使用 `-i` 选项指定输入文件，这里我们指定多个视频文件。
# 4. 使用 `-filter_complex` 选项指定一个复杂的过滤器，这里使用 `concat` 过滤器将多个视频文件连接在一起。
# 5. 使用 `-c:v` 选项指定视频编码器，这里使用 `libx264`。
# 6. 使用 `-c:a` 选项指定音频编码器，这里使用 `aac`。
# 7. 最后，指定输出文件的路径。
# 最后，使用 `subprocess.run` 运行构建好的 `ffmpeg` 命令，并检查命令是否成功执行。
# 在 `__main__` 块中，定义了三个视频文件的路径和一个输出文件的路径，然后调用 `merge_videos` 函数将这三个视频文件合并成一个视频文件。



async def merge_videos(video_paths, output_path):
    # 构建ffmpeg命令
    command = ["ffmpeg", "-y"]
    for video_path in video_paths:
        command.extend(["-i", str(video_path)])
    command.extend([
        "-filter_complex",
        f"concat=n={len(video_paths)}:v=1:a=1",
        "-c:v", "libx264",
        "-c:a", "aac",
        str(output_path)
    ])

    # 运行ffmpeg命令
    subprocess.run(command, check=True)

if __name__ == "__main__":
    video_paths = [
        Path(__file__).parent.parent / "assets/videos/video1.mp4",
        Path(__file__).parent.parent / "assets/videos/video2.mp4",
        Path(__file__).parent.parent / "assets/videos/video3.mp4"
    ]
    output_path = Path(__file__).parent.parent / "assets/videos/merged_video.mp4"
    
    asyncio.run(merge_videos(video_paths, output_path))



