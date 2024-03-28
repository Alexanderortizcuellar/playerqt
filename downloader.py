from pytube import YouTube

downloader = YouTube("https://youtu.be/3cvmONlV5WU")
streams = downloader.streams.first()
streams.download(r"C:\Users\ASUS\qt_programs\player")