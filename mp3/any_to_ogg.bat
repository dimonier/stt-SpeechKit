cd D:\Video\FFMPEG\ffmpeg-2022-02-03-git-e1a14479a8-full_build\bin\
ffmpeg.exe -i "%~dp0%~1" -acodec libopus "%~dp0%~n1.ogg"
