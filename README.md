# Geospatial-Flask-App
A Flask-based web application for geospatial data visualization and analysis, allowing users to upload images, extract EXIF metadata, and view locations on an interactive map.

Features
Image Upload: Upload multiple images to the server.
Metadata Extraction: Extract GPS coordinates, altitude, and camera orientation from images using exifread.
Interactive Map: Display images on a map with markers using Mapbox.

Installation
Clone the repository:

git clone https://github.com/ryangrabo/Geospatial-Flask-App.git
cd Geospatial-Flask-App
Create a virtual environment:
`venv\Scripts\activate`

Install dependencies:
pip install -r requirements.txt

Configuration
Set up environment variables:

Create a .env file in the project root directory and add the necessary environment variables, for example:

bash
Copy code
FLASK_APP=app.py
FLASK_ENV=development
Usage
Run the application:

bash
Copy code
flask run
Open your web browser:

Navigate to http://127.0.0.1:5000 to access the application.

Application Flow
Initialization:

create_app(): Initializes the Flask application and sets up configurations, including the upload folder.
Registers the 'main' Blueprint.
Routing:

routes.py: Defines routes for index page, image uploads, and JSON data of images.
/: Renders the home page.
/upload: Handles image uploads.
/images: Returns image metadata in JSON format.

File Handling:

Uploaded images are saved in static/images.
allowed_file(): Ensures only allowed file types are processed.
Metadata Extraction:

Uses exifread to read EXIF metadata, including GPS coordinates and camera orientation.
Web Interface:

HTML templates (upload.html and index.html) for uploading images and viewing the map.
JavaScript for dynamic features such as image previews and map interactions.
Running the Application:

run.py: Starts the Flask server on port 5001.

Detailed Flow
User navigates to the web application URL:

Browser sends a GET request to the Flask server.
Flask server handles the request and renders the home page.
User uploads images:

Browser sends a POST request with images to /upload.
Flask saves images and extracts metadata.
User views images on the map:

Browser sends a GET request to /images.
Flask responds with a JSON object containing image metadata.
JavaScript processes the JSON response and updates the map with markers.
Mapbox Integration
Collects and processes geospatial data into map tiles.
Provides APIs for accessing map tiles, geocoding services, and more.
Renders and delivers map tiles to the user's device for display.


Acknowledgements
This project uses several open-source libraries and tools, including:

Flask
exifread
Mapbox
