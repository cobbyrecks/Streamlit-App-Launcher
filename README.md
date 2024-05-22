# Streamlit App Launcher

This Streamlit application allows users to seamlessly launch and explore a variety of Streamlit apps from one convenient platform. It provides an intuitive interface for sorting and managing multiple apps, making it easier to access and utilize different Streamlit projects without hassle.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)

## Features

- **Sort Apps**: Sort apps by name, size, date created, or date modified.
- **Upload Apps**: Upload apps from your local machine to the Streamlit App Launcher.
- **Launch Apps**: Launch any selected Streamlit app directly from the interface.
- **User-Friendly Interface**: Simple and intuitive layout with easy-to-use controls.

## Installation

To run this app locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/streamlit-app-launcher.git
    cd streamlit-app-launcher
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start the Streamlit app, run the following command:

```bash
streamlit run app.py
```

Open your web browser and go to [http://localhost:8501](http://localhost:8501) to view the app.

## Example Usage

1. **Select Arrangement Criteria**: Use the drop-down bar to select how you want to sort the apps (Name, Size, Date created, Date modified).
2. **View Sorted Apps**: The main interface will display the apps sorted based on your selected criteria.
3. **Launch an App**: Click the "Launch app" button next to the app you wish to run.

## Configuration

- **Apps Directory**: The app looks for other Streamlit apps in the `streamlit_apps` directory by default. Place your Streamlit app scripts (.py files) in this folder. Or you can use the Upload New Apps section in the sidebar of the Streamlit Launcher to upload the Streamlit apps.
- **Number of Columns**: The number of columns used to display the apps can be configured in the `display_apps` function (`num_columns` variable).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
