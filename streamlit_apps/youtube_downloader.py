import os
import time
import streamlit as st

from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError


def format_length(seconds: int) -> str:
    """Formats video length to 'hh:mm:ss' or 'mm:ss' format."""
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes}:{seconds:02d}"


def format_file_size(bytes: int) -> str:
    """Formats file size in bytes to human-readable format"""
    return f"{bytes / 1024:.2f} KB" if bytes < 1024 * 1024 else f"{bytes / (1024 * 1024):.2f} MB"


def progress_func(stream, chunk, bytes_remaining) -> None:
    """Progress callback to update Streamlit progress bar."""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progress = bytes_downloaded / total_size

    elapsed_time = time.time() - st.session_state.start_time
    speed = bytes_downloaded / elapsed_time if elapsed_time > 0 else 0
    remaining_time = (bytes_remaining / speed) if speed > 0 else 0
    remaining_size_str = format_file_size(bytes_remaining)
    speed_str = format_file_size(speed) + "/s"

    if "progress_bar" in st.session_state:
        st.session_state.progress_bar.progress(progress)
        st.session_state.progress_text.text(
            f"Download Progress: {progress:.1%} - {remaining_size_str} left, {remaining_time:.1f}s remaining, Speed: {speed_str}"
        )


@st.cache_data(show_spinner="**Loading video...**")
def get_video_streams(video_url: str) -> tuple:
    """Fetches video stream using PyTube"""
    yt = YouTube(video_url, on_progress_callback=progress_func)
    video_streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution")
    return yt, video_streams


def download_video(selected_stream, save_path: str, quality: str) -> None:
    """Downloads the selected video stream using PyTube"""
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_name = f"{selected_stream.default_filename.split('.')[0]}_{quality}.mp4"

    # Initialize progress bar and text in Streamlit
    st.session_state.progress_bar = st.progress(0)
    st.session_state.progress_text = st.empty()
    st.session_state.start_time = time.time()

    selected_stream.download(output_path=save_path, filename=file_name)

    # Clear progress bar and text after download completes
    st.session_state.progress_bar.empty()
    st.session_state.progress_text.empty()


def main() -> None:
    """Main function to run the Streamlit application for YouTube Video Downloader."""
    st.title(":red[YouTube Video Downloader]")
    with st.sidebar:
        st.header("**Select Download Option**")
        st.divider()
        st.write("**Choose whether to download a single video or multiple videos**.")

        download_option = st.sidebar.radio("**Select Option**", ("**Single Video**", "**Multiple Videos**"))

    if download_option == "**Single Video**":
        st.divider()
        video_url = st.text_input(label="", placeholder="Enter YouTube video URL")

        if video_url:
            try:
                yt, video_streams = get_video_streams(video_url)

                if video_streams:
                    stream_options = [f"{stream.resolution} ({format_file_size(stream.filesize)})" for stream in video_streams]

                    with st.container(border=True):
                        col1, col2 = st.columns([1, 1.618])

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
                        download_video(selected_stream, save_path, quality)
                        st.success("Video downloaded successfully!")

                else:
                    st.error("No available streams found for this video!")

            except RegexMatchError:
                st.error("Invalid YouTube URL. Please enter a valid URL!")
            except VideoUnavailable:
                st.error("The video is unavailable. Please check the URL and try again!")
            except Exception as error:
                st.error(f"An error occurred!: {error}")

    elif download_option == "**Multiple Videos**":
        st.divider()
        video_urls_input = st.text_area(label="", placeholder="Enter YouTube video URLs (one per line)")

        video_urls = [url.strip() for url in video_urls_input.split("\n") if url.strip()]
        video_streams_data = []

        if video_urls:
            for idx, url in enumerate(video_urls):
                try:
                    yt, video_streams = get_video_streams(url)
                    if video_streams:
                        video_streams_data.append((yt, video_streams))
                    else:
                        st.error(f"No available streams found for video {idx + 1}!")
                except RegexMatchError:
                    st.error(f"Invalid YouTube URL: Video {idx + 1}. Please enter a valid URL!")
                except VideoUnavailable:
                    st.error(f"The video is unavailable: Video {idx + 1}. Please check the URL and try again!")
                except Exception as error:
                    st.error(f"An error occurred!: {error}")

            if video_streams_data:
                quality_selections = []
                for idx, (yt, video_streams) in enumerate(video_streams_data):
                    stream_options = [f"{stream.resolution} ({format_file_size(stream.filesize)})" for stream in video_streams]

                    with st.container(border=True):
                        col1, col2 = st.columns([1, 1.618])

                        # Display video thumbnail
                        with col1:
                            st.image(yt.thumbnail_url, width=200)

                        # Select video quality
                        with col2:
                            st.write(f"**:red[Title:] {yt.title}**")
                            st.write(f"**:red[Length:] {format_length(yt.length)}**")
                            quality = st.selectbox(f"**:red[Select available video quality for video {idx + 1}:]**", stream_options, key=f"quality_{idx}")
                            quality_selections.append((idx, quality))

                if st.button("**Download All Videos**"):
                    for idx, (yt, video_streams) in enumerate(video_streams_data):
                        quality = quality_selections[idx][1]
                        selected_stream = video_streams[[f"{stream.resolution} ({format_file_size(stream.filesize)})" for stream in video_streams].index(quality)]
                        save_path = "downloads"  # Set the save path to the 'downloads' folder
                        quality = quality.split()[0]  # Extract quality from the selected option
                        download_video(selected_stream, save_path, quality)
                        st.success(f"Video {idx + 1} downloaded successfully!")


if __name__ == "__main__":
    main()
