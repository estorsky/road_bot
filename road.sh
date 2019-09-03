#!/bin/bash

if [[ -z "$1" ]]; then exit; fi
if [[ -z "$2" ]]; then exit; fi
if [[ -z "$3" ]]; then exit; fi

MAXSIZE=52428800
# MAXSIZE=5242880
URL=$1
SPEED=$3

convert () {
    youtube-dl -q -w --extract-audio --audio-format mp3 --embed-thumbnail --add-metadata --output '%(title)s.%(ext)s' $URL
    # youtube-dl -q -w --extract-audio --audio-format mp3 --embed-thumbnail --add-metadata --output '%(artist)s.%(ext)s' $URL
    # youtube-dl -w -f 140 --embed-thumbnail --add-metadata --output '%(id)s.%(ext)s' $URL
    # youtube-dl -q -f bestaudio[ext=m4a] --embed-thumbnail --add-metadata $URL
    # youtube-dl -q -w --extract-audio --audio-format mp3 --add-metadata --output '%(id)s.%(ext)s' $URL
    NAME=$(find ./$2 -type f -printf "%f\n")
    FILESIZE=$(stat -c%s "$NAME")
    if [ "$SPEED" != 1 ]; then
        echo speedup
        mv "$NAME" "tmp$NAME"
        ffmpeg -y -loglevel quiet -i "tmp$NAME" -filter:a "atempo=$SPEED" "$NAME"
        rm "tmp$NAME"
    fi
}

split () {
    ffmpeg -y -loglevel quiet -i "$NAME" -map_metadata 0 -f segment -segment_time 3000 -c copy "%d.$NAME"
    rm "$NAME"
}

mkdir ./temp/$2
cd ./temp/$2
convert
if (( FILESIZE > MAXSIZE  )); then
    split
fi

# read
../../translit.sh

