import tkinter as tk
from tkinter import messagebox
from pytube import *
import requests
import tqdm
from tkinter import ttk
#function to download the videos
def start_download():
    playlist_url = url_entry.get()
    save_directory = dir_entry.get()
    #function to get the videos
    def get_playlist (playlists):
        urls=[]
        for playlist in playlists:
            playlist_urls = Playlist(playlist)
            for url in playlist_urls:
                urls.append(url)
        return urls
    #get the number of videos in the playlist
    num_of_vids = len(get_playlist([playlist_url]))
    #loop that goes through all the videos
    for vid_num in tqdm.tqdm(range(num_of_vids), "Downloading Videos"):
        #store videos in an array
        urls = get_playlist([playlist_url])
        # the YouTube video to download
        url = urls[vid_num]
        # Create a YouTube object
        yt = YouTube(url)
        title = yt.title
        video_title.config(text=title)
        # Get the video with the highest resolution available
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        #create a progress bar for the current video being downloaded
        with tqdm.tqdm(unit='B', unit_scale=True, unit_divisor=1024, desc=f'Downloading Video {vid_num+1}') as pbar:
            video_url = video.url
            video_size = video.filesize
            response = requests.get(video_url, stream=True)
            with open(f'{save_directory}/vid_{vid_num+1}.mp4', 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    pbar.update(len(chunk))
                    f.write(chunk)
                    progressbar["value"] = (vid_num / num_of_vids) * 100
                    root.update()
                    speed = response.elapsed.total_seconds()
                    speed_label.config(text=f"Speed: {speed:.2f}s")
    messagebox.showinfo("Success", "All videos have been downloaded successfully!")
root = tk.Tk()
root.title("YouTube Playlist Downloader")
url_label = tk.Label(root, text="Enter the URL of the YouTube playlist:")
url_label.pack()
url_entry = tk.Entry(root)
url_entry.pack()
dir_label = tk.Label(root, text="Enter the directory where you want to save the videos:")
dir_label.pack()
dir_entry = tk.Entry(root)
dir_entry.pack()
progressbar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progressbar.pack()
video_title = tk.Label(root, text="")
video_title.pack()
speed_label = tk.Label(root, text="")
speed_label.pack()
download_button = tk.Button(root, text="Start Download", command=start_download)
download_button.pack()
root.mainloop()