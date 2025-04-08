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
            # Modified to ensure we get formats with both video and audio
            'format': 'best/bestvideo*+bestaudio/best'
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
            # Modified to ensure we get both video and audio
            'format': f'{format_id}+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'no_warnings': True,
            'quiet': True,
            # Add format sorting to prefer formats with audio
            'format_sort': ['hasvid', 'hasaud']
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return f"downloads/{info['title']}.{info['ext']}"
    except Exception as e:
        st.error(f"Error downloading video: {str(e)}")
        return None

def is_valid_youtube_url(url):
    return url and ('youtube.com' in url or 'youtu.be' in url)

def main():
    st.title("YouTube Video Downloader")
    
    # Create downloads directory if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

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
                            st.success("Video downloaded successfully!")
                else:
                    st.warning("No supported video formats found.")
        else:
            st.error("Please enter a valid YouTube URL")

if __name__ == "__main__":
    main()
