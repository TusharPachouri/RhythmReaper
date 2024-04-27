from pytube import YouTube as youtube # type: ignore
import tkinter as tk
import subprocess
from tkinter import filedialog
from pytube import Search

from downloader import downloadMp3, open_file_dialog
from spotify import get_token, search_for_artist, get_songs_of_artist
import os

# search = Search('Night Changes')
# # for i in search.results:
# #     print(i.watch_url)
# #     print('-------------------')

# # keys = "\n".join([k for k in search.results[0].__dict__])
# # print(keys)
# print(search.results[0].watch_url)

# yt = youtube(search.results[0].watch_url)


if __name__ == "__main__":
    #tkinter code
    root = tk.Tk()
    root.title("YouTube Video Downloader")
    root.withdraw()
    # url = input("Enter the URL of the video: ")
    
    token_spotify = get_token() # Spotify token

    singer = str(input("Enter the name of the singer: ")) # Singer name

    result = search_for_artist(token_spotify, singer) # Search for the singer
    
    artist_id = result["id"] # Get the artist ID

    songs = get_songs_of_artist(token_spotify, artist_id)
    
    directory = open_file_dialog() # Open file dialog to select directory
    path = os.path.join(directory, singer) 

    if not os.path.exists(path):
        os.makedirs(path)
        path = os.path.join(directory, singer)

    if directory:
        print("Downloading video to %s" % directory)
        for idx, song in enumerate(songs):
            # print(f"{idx+1}. {song['name']}")
            search = Search(song['name'])
            url = search.results[0].watch_url
            print("Downloading song %s" % song['name'])
            # print(url)
            downloadMp3(url, path)
            # print("Download complete.")
    else:
        print("No directory selected. Exiting...")
        
    subprocess.run(["pkill", "-f", "python"])