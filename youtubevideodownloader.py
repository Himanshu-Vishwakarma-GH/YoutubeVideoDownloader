import streamlit as st
import yt_dlp
import os
from datetime import timedelta

def format_duration(seconds):
    return str(timedelta(seconds=seconds))

def get_video_info(url):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'format': 'best/bestvideo*+bestaudio/best',
            'cookiefile': 'cookies.txt',  # Use cookies to bypass restrictions
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            },
            'noplaylist': True,  # Ensure only the video is processed
            #'proxy': 'http://your-proxy-server:port',  # Replace with a valid proxy
            'verbose': True  # Enable debugging to see detailed logs
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            
            # Get all available formats
            all_formats = info.get('formats', [])
            
            # Filter for formats with both video and audio
            for f in all_formats:
                # Ensure format has both video and audio
                if f.get('acodec') != 'none' and f.get('vcodec') != 'none':
                    height = f.get('height', 0)
                    if height in [360, 480, 720, 1080]:
                        # Avoid duplicate resolutions
                        if not any(existing['height'] == height for existing in formats):
                            formats.append({
                                'format_id': f['format_id'],
                                'height': height,
                                'ext': f.get('ext', 'mp4'),
                                'format_note': f.get('format_note', '')
                            })
            
            # Sort formats by resolution (highest first)
            formats.sort(key=lambda x: x['height'], reverse=True)
            
            # If no formats found, use best available with audio
            if not formats:
                best_format = next((f for f in all_formats 
                                  if f.get('acodec') != 'none' 
                                  and f.get('vcodec') != 'none'), None)
                if best_format:
                    formats.append({
                        'format_id': best_format['format_id'],
                        'height': best_format.get('height', 720),
                        'ext': best_format.get('ext', 'mp4'),
                        'format_note': best_format.get('format_note', '')
                    })
            
            return {
                'title': info['title'],
                'thumbnail': info['thumbnail'],
                'duration': info['duration'],
                'formats': formats
            }
    except Exception as e:
        st.error(f"Error fetching video info: {str(e)}")
        return None

def download_video(url, format_id):
    try:
        ydl_opts = {
            'format': f'{format_id}+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',  # Save in the current directory
            'no_warnings': True,
            'quiet': True,
            'cookiefile': 'cookies.txt',  # Use cookies to bypass restrictions
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            },
            'noplaylist': True,  # Ensure only the video is processed
            #'proxy': 'http://your-proxy-server:port',  # Replace with a valid proxy
            'verbose': True  # Enable debugging to see detailed logs
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return f"{info['title']}.{info['ext']}"  # Return the file name
    except Exception as e:
        st.error(f"Error downloading video: {str(e)}")
        return None

def is_valid_youtube_url(url):
    return url and ('youtube.com' in url or 'youtu.be' in url)

def main():
    st.title("YouTube Video Downloader")
    
    url = st.text_input("Enter YouTube Video URL")

    if url:
        if is_valid_youtube_url(url):
            video_info = get_video_info(url)
            
            if video_info:
                st.image(video_info['thumbnail'], width=400)
                st.write(f"**{video_info['title']}**")
                st.write(f"Duration: {format_duration(video_info['duration'])}")
                
                if video_info['formats']:
                    # Resolution selection
                    available_resolutions = [f"{f['height']}p" for f in video_info['formats']]
                    selected_resolution = st.selectbox(
                        "Select Resolution", 
                        available_resolutions
                    )
                    
                    # Download button
                    if st.button("Download Video"):
                        selected_format = next(
                            f['format_id'] for f in video_info['formats'] 
                            if f"{f['height']}p" == selected_resolution
                        )
                        
                        video_path = download_video(url, selected_format)
                        
                        if video_path and os.path.exists(video_path):
                            with open(video_path, "rb") as file:
                                st.download_button(
                                    label="Save Video to Device",
                                    data=file,
                                    file_name=os.path.basename(video_path),
                                    mime="video/mp4"
                                )
                            st.success("Video is ready for download!")
                            os.remove(video_path)  # Clean up after download
                else:
                    st.warning("No supported video formats found.")
        else:
            st.error("Please enter a valid YouTube URL")

if __name__ == "__main__":
    main()
