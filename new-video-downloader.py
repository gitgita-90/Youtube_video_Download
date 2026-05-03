import os
import subprocess
import sys

def update_yt_dlp():
    """Cleans the local cache and forces a reinstall of the latest yt_dlp."""
    print("[*] Checking for yt_dlp updates and repairing dependencies...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "--force-reinstall", "yt_dlp", "--quiet"],
            check=True
        )
        print("[+] yt_dlp updated and verified successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to update yt_dlp: {e}")

# yt_dlp imported after the verification/installation step
import yt_dlp as youtube_dl

def download_audio(url, quality):
    """Downloads and converts YouTube audio to MP3 format."""
    audio_format = {
        '128k': 'bestaudio[abr<=128k]',
        '256k': 'bestaudio/best',
    }
    
    output_path = r'E:\New folder/'
    
    ydl_opts = {
        'format': audio_format[quality],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '256' if quality == '256k' else quality[:-1],
        }],
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_video(url, resolution):
    """Downloads the best video and audio combination matching the specified resolution."""
    video_format = {
        '360p': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '1440p': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
        '2160p': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]',
        '4320p': 'bestvideo[height<=4320]+bestaudio/best[height<=4320]',
        '8640p': 'bestvideo[height<=8640]+bestaudio/best[height<=8640]',
        '15360p': 'bestvideo[height<=15360]+bestaudio/best[height<=15360]',
    }
    
    output_path = r'E:\New folder/'
    
    ydl_opts = {
        'format': video_format[resolution],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    url = input("Enter the URL of the audio/video: ").strip()
    choice = input("Do you want to download (1) Audio or (2) Video? ").strip()

    if choice == '1':
        quality = input("Choose quality (128k or 256k): ").strip()
        if quality in ['128k', '256k']:
            download_audio(url, quality)
            print("Audio downloaded successfully.")
        else:
            print("Invalid quality selected.")
    
    elif choice == '2':
        resolution = input("Choose resolution (360p, 480p, 720p, 1080p, 1440p, 2160p, 4320p, 8640p, 15360p): ").strip()
        if resolution in ['360p', '480p', '720p', '1080p', '1440p', '2160p', '4320p', '8640p', '15360p']:
            download_video(url, resolution)
            print("Video downloaded successfully.")
        else:
            print("Invalid resolution selected.")
    
    else:
        print("Invalid choice. Please enter 1 for audio or 2 for video.")

if __name__ == '__main__':
    # Ensure the target directory exists
    target_dir = r'E:\New folder'
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    # Run the installation and update command before starting the main logic
    update_yt_dlp()
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Program interrupted by user.")