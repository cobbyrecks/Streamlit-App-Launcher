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


def get_sorted_apps(apps_directory: str, arrange_by: str) -> List[str]:
    """Sort apps based on the selected criteria"""
    apps = os.listdir(apps_directory)
    if arrange_by == "Name":
        sorted_apps = sorted(apps)
    elif arrange_by == "Size":
        sorted_apps = sorted(apps, key=lambda app: get_file_size(os.path.join(apps_directory, app)))
    elif arrange_by == "Date created":
        sorted_apps = sorted(apps, key=lambda app: get_date_created(os.path.join(apps_directory, app)))
    elif arrange_by == "Date modified":
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
            st.header(f":blue[{os.path.splitext(app_name)[0]}]")
            if st.button("Launch app", key=idx):
                launch_app(os.path.join(apps_directory, app_name))


# Streamlit UI
def main() -> None:
    st.title("Streamlit App Launcher")
    with st.sidebar:
        arrange_by = st.selectbox("Arrange apps by:",
                                  ("Name", "Size", "Date created", "Date modified",))

    st.write("")
    st.write("")
    st.write(f"Apps sorted by {arrange_by.lower()}")

    apps_directory = "example_apps"  # put your streamlit apps (.py) in this folder
    sorted_apps = get_sorted_apps(apps_directory, arrange_by)

    num_columns = 2
    display_apps(sorted_apps, apps_directory, num_columns)


if __name__ == "__main__":
    main()
