# YouTube Video Downloader

A Streamlit-based application that allows users to download YouTube videos in various resolutions with both video and audio.

## Features

- Download YouTube videos in multiple resolutions (360p, 480p, 720p, 1080p)
- Preview video thumbnail before downloading
- Show video duration and title
- Simple and user-friendly interface
- Downloads include both video and audio tracks
- Supports direct download to local device

## Requirements

```bash
streamlit
yt-dlp
python-dateutil
```

## Installation

1. Clone the repository
```bash
git clone <your-repository-url>
cd video-scrap
```

2. Install required packages
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run scrap.py
```

2. Enter a YouTube video URL in the input field
3. Select your preferred video resolution
4. Click "Download Video"
5. Save the video to your device

## Project Structure

```
video-scrap/
│
├── scrap.py          # Main application file
├── requirements.txt  # Python dependencies
├── README.md        # Project documentation
└── downloads/       # Download directory (created automatically)
```

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web interface
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video extraction

## Author

[Your Name]

## Disclaimer

This tool is for educational purposes only. Please respect YouTube's terms of service and content creators' rights when using this application.