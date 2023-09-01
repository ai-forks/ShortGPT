#!/bin/bash


#yt-dlp --proxy socks5://172.17.0.1:1080 -f22+140 https://www.youtube.com/watch?v=V6l4E9tZ7u4 -o '%(title)s-%(id)s.mp4'
echo "args: url=[$1] proxy=[$PROXY]"
if [ -n $PROXY ]; then
    echo "use proxy"
    yt-dlp --proxy $PROXY -f22+140 $1 -o '%(title)s-%(id)s.mp4'
else
    echo "no proxy"
    yt-dlp -f22+140 $1 -o '%(title)s-%(id)s.mp4'
fi
