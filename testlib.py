
import subprocess
from moviepy.editor import (AudioFileClip, CompositeVideoClip,CompositeAudioClip, ImageClip,
                            TextClip, VideoFileClip, vfx,)
from shortGPT.audio.audio_duration import getYoutubeVideoLink
from shortGPT.api_utils.pexels_api import search_videos
from shortGPT.editing_utils.handle_videos import downloadYoutubeVideo, get_video_duration
import re
import hashlib
import datetime
import os

def test_ffmpeg():
    print(f"==============test lib ffmpeg")
    #ffmpeg -hwaccel cuvid  -i v1_cut.mp4 -c:v h264_nvenc -b:v 2048k -vf scale_npp=1280:-1 -y outputs/x3.mp4
    start_time=100.10
    clip_duration=60
    commond = [
        'ffmpeg', 
        "-hwaccel", "cuvid",
        "-i", "/app/public/vv2.mp4",
        "-ss", str(start_time),  
        "-t", str(clip_duration),
        "-c:v", "h264_nvenc",
        "-b:v", "2048k",
        "-vf", "scale_npp=1280:-1",
        "-y",
        "/app/videos/xx.gpt.mp4"
    ]
    print(f"commond={' '.join(commond)}")
    subprocess.run(commond)

def test_moviepy_editor():
    print(f"==============test lib moviepy_editor imagemagick ghostscript")
    text_clip_params = {'text': 'REDDIT你生活中最大的无脸时刻是什么有一次我参加了一个派对对一个女孩有着强烈的喜欢我们暂且叫她爱迷力吧于是我骨足了勇气决定行动起来我走向她感觉自己很牛逼然后说到嘿你掉了东西她一脸困惑地看着我问什么东西你知道我干了什么吗我指着她的心脏说我的下巴很流畅对吧然后整个房间都变得安静下来每个人都丁着我看我感觉脸上火拉拉的爱迷力去放生大笑起来结果那个女孩并不是爱迷力而是她的长得一模一样的双胞胎姐姐爱马我真想找个地方专进去再也不出来了这可真是给人留下了一个糟糕的低印象朋友们这是我一生中最大的无脸时刻', 'fontsize': 100, 'font': 'Calibri-Bold', 'color': 'white', 'stroke_width': 3, 'stroke_colr': 'black', 'method': 'caption', 'size': [900, None]}
    text_clip_params['txt'] = text_clip_params["text"]
    clip_info = {k: text_clip_params[k] for k in ('txt', 'fontsize', 'font', 'color', 'stroke_width', 'stroke_color', 'size', 'kerning', 'method', 'align') if k in text_clip_params}
    print(f"process_text_asset {text_clip_params}")
    clip = TextClip(**clip_info)

def test_youtube():
    url, duration = getYoutubeVideoLink("https://www.youtube.com/watch?v=V6l4E9tZ7u4")
    print(f"test_youtube url=[{url}]")


def test_pexels():
    json_data = search_videos("中国女孩")
    print(f"test_pexels={json_data}")

def test_download():
    #url = "https://www.youtube.com/watch?v=V6l4E9tZ7u4"
    url = " https://player.vimeo.com/external/516795301.hd.mp4?s=b0c2091d3380693ee1e89f35a5ba821dc547ec80&profile_id=175&oauth2_token_id=57447761"
    #outputFile,duration = downloadYoutubeVideo(url)
    #print(f"test_download outputFile={outputFile} duration={duration}")
    outputFile="/app/videos/dl/2023/09/02/4ed84730d72f875b988e557e48a5818d.mp4"
    duration = get_video_duration(outputFile)
    print(f"video duration={duration}")

test_download()
#test_ffmpeg()
#test_moviepy_editor()
#test_youtube()
#test_pexels()
