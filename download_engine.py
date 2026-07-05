import os
import re
from yt_dlp import YoutubeDL

def clean_filename(name):
    """Removes restricted characters to ensure clean local filenames."""
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_hd_track(search_query, output_folder="music/downloads"):
    """
    Takes an AI search query, dynamically searches YouTube,
    extracts the highest quality audio, and converts it to a 320kbps MP3 via FFmpeg.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"📁 Created folder: {output_folder}")
        
    ydl_opts = {
        'format': 'bestaudio/best',  # Targets the absolute best audio stream
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',  # Forces standard high-fidelity 320kbps compression
        }],
        'quiet': False,
        'cookiefile': 'cookies.txt'
    }
    
    search_string = f"ytsearch1:{search_query}"
    print(f"\n🔍 Agent searching database for: '{search_query}'...")
    
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(search_string, download=True)
            if 'entries' in info and len(info['entries']) > 0:
                video_title = info['entries'][0]['title']
                clean_title = clean_filename(video_title)
                final_path = os.path.join(output_folder, f"{clean_title}.mp3")
                print(f"✅ Success! Saved to: {final_path}")
                return final_path
        except Exception as e:
            print(f"❌ Downloader error: {e}")
            return None

if __name__ == "__main__":
    # Quick test run query
    download_hd_track("mango flame")