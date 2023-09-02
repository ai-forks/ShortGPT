import ffmpeg
import os
import random
import yt_dlp
import subprocess
import json
import hashlib
import datetime

def getYoutubeVideoLink(url):
    if 'shorts' in url:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "no_color": True,
            "no_call_home": True,
            "no_check_certificate": True,
            "format": "bestvideo[height<=1920]",
            "proxy": os.environ['PROXY'] if 'PROXY' in os.environ else ""
        }
    else:
        ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "no_color": True,
        "no_call_home": True,
        "no_check_certificate": True,
        "format": "bestvideo[height<=1080]",
        "proxy": os.environ['PROXY'] if 'PROXY' in os.environ else ""
        }
    try:
        print(f"===>download youtube url={url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            dictMeta = ydl.extract_info(
                url,
                download=False)
            return dictMeta['url'], dictMeta['duration']
    except Exception as e:
        print("Failed getting video link from the following video/url", e.args[0])
    return None, None

def downloadYoutubeVideo(url):
    outputFile = "/app/videos/dl/"+datetime.datetime.now().strftime('%Y/%m/%d')+"/"+ hashlib.md5(url.encode()).hexdigest()+".mp4"
    pyt = re.compile('.*youtube\.com')
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "no_color": True,
        "no_call_home": True,
        "no_check_certificate": True,
        "format": "bestvideo[width<=1080]" if pyt.match(video_url) else 'mp4' ,
        "outtmpl": outputFile,
        "tries": "333",
        "proxy": os.environ['PROXY'] if 'PROXY' in os.environ else ""
    }
    try:
        print(f"===>download youtube url={url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            dictMeta = ydl.extract_info(
                url,
                download=True)
            return outputFile, dictMeta['duration']
    except Exception as e:
        print("Failed getting video link from the following video/url", e.args[0])
    return None, None

def extract_random_clip_from_video(video_url, video_duration, clip_duration , output_file):
    print(video_url, video_duration, clip_duration , output_file)
    """Extracts a clip from a video using a signed URL.
    Args:
        video_url (str): The signed URL of the video.
        video_url (int): Duration of the video.
        start_time (int): The start time of the clip in seconds.
        clip_duration (int): The duration of the clip in seconds.
        output_file (str): The output file path for the extracted clip.
    """
    if not video_duration:
        raise Exception("Could not get video duration")
    if not video_duration*0.7 > 120:
        raise Exception("Video too short")
    start_time = video_duration*0.15 + random.random()* (0.7*video_duration-clip_duration)
    print(f"output video input={video_url} output={output_file} start_time={start_time} ")
    """     (
        ffmpeg
        .input(video_url, ss=start_time, t=clip_duration)
        .output(output_file, codec="libx264", preset="ultrafast")
        .run()
    ) """
    commond = [
        'ffmpeg', 
        "-hwaccel", "cuvid",
        "-i", video_url,
        "-ss", str(start_time),  
        "-t", str(clip_duration),
        "-c:v", "h264_nvenc",
        "-b:v", "2048k",
        "-vf", "scale_npp=1280:-1",
        "-y",
        output_file
    ]
    print(f"commond={' '.join(commond)}")
    subprocess.run(commond)
    if not os.path.exists(output_file):
        raise Exception("Random clip failed to be written")
    return output_file


def get_aspect_ratio(video_file):
    cmd = 'ffprobe -i "{}" -v quiet -print_format json -show_format -show_streams'.format(video_file)
#     jsonstr = subprocess.getoutput(cmd)
    jsonstr = subprocess.check_output(cmd, shell=True, encoding='utf-8')
    r = json.loads(jsonstr)
    # look for "codec_type": "video". take the 1st one if there are mulitple
    video_stream_info = [x for x in r['streams'] if x['codec_type']=='video'][0]
    if 'display_aspect_ratio' in video_stream_info and video_stream_info['display_aspect_ratio']!="0:1":
        a,b = video_stream_info['display_aspect_ratio'].split(':')
        dar = int(a)/int(b)
    else:
        # some video do not have the info of 'display_aspect_ratio'
        w,h = video_stream_info['width'], video_stream_info['height']
        dar = int(w)/int(h)
        ## not sure if we should use this
        #cw,ch = video_stream_info['coded_width'], video_stream_info['coded_height']
        #sar = int(cw)/int(ch)
    if 'sample_aspect_ratio' in video_stream_info and video_stream_info['sample_aspect_ratio']!="0:1":
        # some video do not have the info of 'sample_aspect_ratio'
        a,b = video_stream_info['sample_aspect_ratio'].split(':')
        sar = int(a)/int(b)
    else:
        sar = dar
    par = dar/sar
    return dar