
import subprocess
from moviepy.editor import (AudioFileClip, CompositeVideoClip,CompositeAudioClip, ImageClip,
                            TextClip, VideoFileClip, vfx,)



# subprocess.run(commond)
def test_ffmpeg():
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

def test_moviepy_editor():
    text_clip_params = {'text': 'REDDIT你生活中最大的无脸时刻是什么有一次我参加了一个派对对一个女孩有着强烈的喜欢我们暂且叫她爱迷力吧于是我骨足了勇气决定行动起来我走向她感觉自己很牛逼然后说到嘿你掉了东西她一脸困惑地看着我问什么东西你知道我干了什么吗我指着她的心脏说我的下巴很流畅对吧然后整个房间都变得安静下来每个人都丁着我看我感觉脸上火拉拉的爱迷力去放生大笑起来结果那个女孩并不是爱迷力而是她的长得一模一样的双胞胎姐姐爱马我真想找个地方专进去再也不出来了这可真是给人留下了一个糟糕的低印象朋友们这是我一生中最大的无脸时刻', 'fontsize': 100, 'font': 'Calibri-Bold', 'color': 'white', 'stroke_width': 3, 'stroke_colr': 'black', 'method': 'caption', 'size': [900, None]}
    text_clip_params['txt'] = text_clip_params["text"]
    clip_info = {k: text_clip_params[k] for k in ('txt', 'fontsize', 'font', 'color', 'stroke_width', 'stroke_color', 'size', 'kerning', 'method', 'align') if k in text_clip_params}
    print(f"process_text_asset {text_clip_params}")
    clip = TextClip(**clip_info)

test_ffmpeg()
test_moviepy_editor()