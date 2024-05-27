import os
import streamlit as st

from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError


@st.cache_data(show_spinner="**Loading video...**")
def get_video_streams(video_url: str) -> tuple:
    """Fetches video stream using PyTube"""
    yt = YouTube(video_url)
    video_streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution")
    return yt, video_streams


def download_video(selected_stream: YouTube.streams, save_path: str, quality: str) -> None:
    """Downloads the selected video stream"""
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_name = f"{selected_stream.default_filename.split('.')[0]}_{quality}.mp4"
    selected_stream.download(output_path=save_path, filename=file_name)


def format_length(seconds: int) -> str:
    """Formats video length to 'hh:mm:ss' or 'mm:ss' format."""
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes}:{seconds:02d}"


def format_file_size(bytes: int) -> str:
    """Formats file size in bytes to human-readable format"""
    return f"{bytes / 1024:.2f} KB" if bytes < 1024 * 1024 else f"{bytes / (1024 * 1024):.2f} MB"


def main() -> None:
    """ Main function to run the Streamlit application for YouTube Video Downloader."""
    st.title(":red[YouTube Video Downloader]")
    st.divider()

    video_url = st.text_input(label="", placeholder="Enter YouTube video URL")

    if video_url:
        try:
            yt, video_streams = get_video_streams(video_url)

            if video_streams:
                stream_options = [f"{stream.resolution} ({format_file_size(stream.filesize)})" for stream in video_streams]

                with st.container(border=True):
                    col1, col2 = st.columns([1, 1.618])  # Lol, the golden ratio; for aesthetics

                    # Display video thumbnail
                    with col1:
                        st.image(yt.thumbnail_url, width=200)

                    # Select video quality
                    with col2:
                        st.write(f"**:red[Title:] {yt.title}**")
                        st.write(f"**:red[Length:] {format_length(yt.length)}**")
                        quality = st.selectbox("**:red[Select available video quality:]**", stream_options)
                        selected_stream = video_streams[stream_options.index(quality)]

                # Download button
                if st.button("**Download**"):
                    save_path = "downloads"  # Set the save path to the 'downloads' folder
                    quality = quality.split()[0]  # Extract quality from the selected option
                    with st.spinner("**Downloading video...**"):
                        download_video(selected_stream, save_path, quality)
                    st.success(f"Video downloaded successfully!")
            else:
                st.error("No available streams found for this video!")

        except RegexMatchError:
            st.error("Invalid YouTube URL. Please enter a valid URL!")
        except VideoUnavailable:
            st.error("The video is unavailable. Please check the URL and try again!")
        except Exception:
            st.error("An error occurred!")


if __name__ == "__main__":
    main()
