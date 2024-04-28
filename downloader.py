from pytube import YouTube as youtube # type: ignore
import tkinter as tk
import subprocess
from tkinter import filedialog
import os

def downloadMp4HighestQuality(url, directory):
    try:
        yt = youtube(url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4")
        highest_res_stream = yt.streams.get_highest_resolution()
        highest_res_stream.download(output_path=directory)
    except Exception as e:
        print("Error: %s" % e)

def downloadMp3(url, directory):
    try:
        yt = youtube(url)
        video = yt.streams.filter(only_audio=True).first()
        # highest_res_stream = yt.streams.get_highest_resolution()
        out_file = video.download(output_path=directory)
        base, ext = os.path.splitext(out_file) 
        new_file = base + '.mp3'
        os.rename(out_file, new_file) 
        print(f"Downloaded to {yt.title}")
    except Exception as e:
        print("Error: %s" % e)

def open_file_dialog():
    folder = filedialog.askdirectory()
    if folder:
        print("Selected folder: %s" % folder)
    return folder

# if __name__ == "__main__":
#     #tkinter code
#     root = tk.Tk()
#     root.title("YouTube Video Downloader")
#     root.withdraw()
#     url = input("Enter the URL of the video: ")
    
#     directory = open_file_dialog() # Open file dialog to select directory

#     if directory:
#         print("Downloading video to %s" % directory)
#         downloadMp3(url, directory)
#         print("Download complete.")
#     else:
#         print("No directory selected. Exiting...")
        
#     # subprocess.run(["pkill", "-f", "python"])