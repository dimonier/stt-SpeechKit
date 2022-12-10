cd D:\Video\FFMPEG\ffmpeg-2022-02-03-git-e1a14479a8-full_build\bin\
ffmpeg.exe -i "%~dp0%~1" -ac 1 -ar 32000 -b:a 40k "%~dp0%~n1.mp3"

rem -ac 1 -ar 32000 -b:a 48k -acodec libopus 