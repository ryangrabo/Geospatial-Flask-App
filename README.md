
# Geospatial Flask App

A Flask-based web application for geospatial data visualization and analysis, allowing users to upload images, extract EXIF metadata, and view locations on an interactive map.

## Features

- **Image Upload**: Upload multiple images to the server.
- **Metadata Extraction**: Extract GPS coordinates, altitude, and camera orientation from images using `exifread`. Using exiftool.exe to extract camera pitch. 
- **Interactive Map**: Display images on a map with markers using Mapbox.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/ryangrabo/Geospatial-Flask-App.git
    cd Geospatial-Flask-App
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Set up environment variables:**

    Create a `.env` file in the project root directory and add the necessary environment variables, for example:

    ```bash
    FLASK_APP=app.py
    FLASK_ENV=development
    ```

## Usage

1. **Run the application:**

    ```bash
    python run.py
    ```

2. **Open your web browser:**

    Navigate to `http://127.0.0.1:5000` to access the application.

## Application Flow

1. **Initialization**:
    - `create_app()`: Initializes the Flask application and sets up configurations, including the upload folder.
    - Registers the 'main' Blueprint.

2. **Routing**:
    - `routes.py`: Defines routes for index page, image uploads, and JSON data of images.
    - `/`: Renders the home page.
    - `/upload`: Handles image uploads.
    - `/images`: Returns image metadata in JSON format.

3. **File Handling**:
    - Uploaded images are saved in `static/images`.
    - `allowed_file()`: Ensures only allowed file types are processed.

4. **Metadata Extraction**:
    - Uses `exifread` to read EXIF metadata, including GPS coordinates and camera orientation.

5. **Web Interface**:
    - HTML templates (`upload.html` and `index.html`) for uploading images and viewing the map.
    - JavaScript for dynamic features such as image previews and map interactions.

6. **Running the Application**:
    - `run.py`: Starts the Flask server on port 5001.

## Detailed Flow

1. **User navigates to the web application URL**:
    - Browser sends a GET request to the Flask server.
    - Flask server handles the request and renders the home page.

2. **User uploads images**:
    - Browser sends a POST request with images to `/upload`.
    - Flask saves images and extracts metadata.

3. **User views images on the map**:
    - Browser sends a GET request to `/images`.
    - Flask responds with a JSON object containing image metadata.
    - JavaScript processes the JSON response and updates the map with markers.

## Mapbox Integration

- Collects and processes geospatial data into map tiles.
- Provides APIs for accessing map tiles, geocoding services, and more.
- Renders and delivers map tiles to the user's device for display.

## Acknowledgements

This project uses several open-source libraries and tools, including:
- Flask
- exifread
- Mapbox