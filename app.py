import os
import subprocess
import streamlit as st

from typing import List


def get_file_size(file_path: str) -> int:
    """Get the size of the app"""
    return os.path.getsize(file_path)


def get_date_created(file_path: str) -> float:
    """Get the creation date of the app"""
    return os.path.getctime(file_path)


def get_date_modified(file_path: str) -> float:
    """Get the latest modified date of the app"""
    return os.path.getmtime(file_path)


def get_sorted_apps(apps_directory: str, sort_by: str) -> List[str]:
    """Sort apps based on the selected criteria"""
    apps = os.listdir(apps_directory)
    if sort_by == "Name":
        sorted_apps = sorted(apps)
    elif sort_by == "Size":
        sorted_apps = sorted(apps, key=lambda app: get_file_size(os.path.join(apps_directory, app)))
    elif sort_by == "Date created":
        sorted_apps = sorted(apps, key=lambda app: get_date_created(os.path.join(apps_directory, app)))
    elif sort_by == "Date modified":
        sorted_apps = sorted(apps, key=lambda app: get_date_modified(os.path.join(apps_directory, app)))
    return sorted_apps


def launch_app(app_file: str) -> None:
    """Launch the app"""
    subprocess.Popen(["streamlit", "run", app_file])


def display_apps(sorted_apps: List[str], apps_directory: str, num_columns: int) -> None:
    """Display the sorted apps"""
    cols = st.columns(num_columns)
    for idx, app_name in enumerate(sorted_apps):
        column_idx = idx % num_columns
        container = cols[column_idx].container(border=True)
        with container:
            # st.header(f":blue[{os.path.splitext(app_name)[0]}]")
            st.markdown(
                f"""
                <div style='position: relative;'>
                    <div style='position: absolute; top: 0; left: 0; font-size: 1.2em; font-weight: bold;'>{idx + 1}</div>
                    <div style='padding-top: 20px;'>
                        <h3 style='color: #1f77b4;'>{os.path.splitext(app_name)[0]}</h3>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("Launch app", key=idx):
                launch_app(os.path.join(apps_directory, app_name))


def upload_apps(apps_directory: str) -> None:
    """Upload new Streamlit apps"""
    uploaded_files = st.file_uploader("Select your Streamlit apps", type="py", accept_multiple_files=True)
    if uploaded_files:
        if st.button("Upload Apps"):
            for uploaded_file in uploaded_files:
                file_name = uploaded_file.name
                with open(os.path.join(apps_directory, file_name), "wb") as f:
                    f.write(uploaded_file.getvalue())
            st.success("Upload successful!")


# Streamlit UI
def main() -> None:
    st.title("Streamlit App Launcher")

    with st.sidebar:
        st.header("Upload New Apps")
        st.divider()
        apps_directory = "streamlit_apps"  # put your streamlit apps (.py) in this folder
        upload_apps(apps_directory)

    st.divider()
    st.write("")
    st.write("")

    with st.popover("Sort apps by"):
        sort_by = st.radio("Options", ("Name", "Size", "Date created", "Date modified"))

    apps_directory = "streamlit_apps"  # put your streamlit apps (.py) in this folder
    sorted_apps = get_sorted_apps(apps_directory, sort_by)

    num_columns = 2
    display_apps(sorted_apps, apps_directory, num_columns)


if __name__ == "__main__":
    main()
