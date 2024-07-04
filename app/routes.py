import os
import exifread
import logging
from flask import Flask, Blueprint, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename

bp = Blueprint('main', __name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Ensure the 'uploads' directories exist
UPLOAD_FOLDERS = [
    os.path.abspath(os.path.join(bp.root_path, 'static', 'images', 'range_40_50')),
    os.path.abspath(os.path.join(bp.root_path, 'static', 'images', 'range_55_65'))
]
for folder in UPLOAD_FOLDERS:
    os.makedirs(folder, exist_ok=True)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

# Differential offset values
LATITUDE_OFFSET = 0.00004  # Adjust this value as needed
LONGITUDE_OFFSET = 0.00  # Adjust this value as needed

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/images')
def get_images():
    images = []

    for folder in UPLOAD_FOLDERS:
        for filename in os.listdir(folder):
            if filename.lower().endswith('.jpg'):
                filepath = os.path.join(folder, filename)
                with open(filepath, 'rb') as f:
                    tags = exifread.process_file(f)

                    gps_latitude = tags.get('GPS GPSLatitude')
                    gps_longitude = tags.get('GPS GPSLongitude')
                    gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
                    gps_longitude_ref = tags.get('GPS GPSLongitudeRef')
                    gps_altitude = tags.get('GPS GPSAltitude')
                    gps_img_direction = tags.get('GPS GPSImgDirection')

                    if gps_latitude and gps_longitude and gps_latitude_ref and gps_longitude_ref:
                        lat = convert_to_degrees(gps_latitude, gps_latitude_ref.values)
                        lon = convert_to_degrees(gps_longitude, gps_longitude_ref.values)
                        yaw = float(gps_img_direction.values[0].num) / float(gps_img_direction.values[0].den) if gps_img_direction else 'Unknown'

                        # Apply differential offset
                        lat -= LATITUDE_OFFSET
                        lon -= LONGITUDE_OFFSET

                        # Use geoid altitude and convert it to feet, rounded to the nearest whole number
                        altitude_meters = gps_altitude.values[0].num / gps_altitude.values[0].den if gps_altitude else None
                        altitude_feet = round(altitude_meters * 3.28084) if altitude_meters else 'undefined'

                        logging.debug(f"Image: {filename}, Latitude: {lat}, Longitude: {lon}, Yaw: {yaw}, Altitude: {altitude_feet} feet")

                        images.append({
                            'filename': filename,
                            'lat': lat,
                            'lon': lon,
                            'yaw': yaw,
                            'alt': altitude_feet
                        })

    return jsonify(images)

def convert_to_degrees(value, ref):
    d = value.values[0].num / value.values[0].den
    m = value.values[1].num / value.values[1].den
    s = value.values[2].num / value.values[2].den
    result = d + (m / 60.0) + (s / 3600.0)
    if ref in ['S', 'W']:
        result = -result
    return result

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        files = request.files.getlist('file')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDERS[0], filename))  # Save to the first folder for simplicity
        return redirect(url_for('main.index'))
    return render_template('upload.html')
