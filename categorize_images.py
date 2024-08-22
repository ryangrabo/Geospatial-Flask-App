import os
import shutil
import subprocess
import json
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Ensure the 'uploads' directories exist
#TODO: Change image paths
UPLOAD_FOLDERS = {
    'phragmites': os.path.abspath('app\static/images/phragmites'),
    'narrowleaf_cattail': os.path.abspath('app\static/images/narrowleaf_cattail'),
    'yellow_iris': os.path.abspath('app\static/images/yellow_iris'),
    #exclude yellow iris, include purple loostrife
    'main': os.path.abspath('app\static/images')
}
for folder in UPLOAD_FOLDERS.values():
    os.makedirs(folder, exist_ok=True)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_metadata_exiftool(filepath):
    command = [
        'exiftool.exe',  # Update with the correct path to exiftool.exe
        '-json',
        filepath
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        metadata = json.loads(result.stdout)[0]
        return {
            'DateTimeOriginal': metadata.get('DateTimeOriginal')
        }
    return {}

def get_image_date_taken(filepath):
    metadata = get_metadata_exiftool(filepath)
    date_taken = metadata.get('DateTimeOriginal')
    if date_taken:
        return date_taken.split()[0].replace(':', '-')  # Format date as YYYY-MM-DD
    return None

def move_image(filename, category, date_taken):
    source_path = os.path.join(UPLOAD_FOLDERS['main'], filename)
    date_folder = os.path.join(UPLOAD_FOLDERS[category], date_taken)
    os.makedirs(date_folder, exist_ok=True)
    dest_path = os.path.join(date_folder, filename)
    shutil.move(source_path, dest_path)
    logging.info(f'Moved {filename} to {date_folder}')

def categorize_images():
    image_folder = UPLOAD_FOLDERS['main']
    for filename in os.listdir(image_folder):
        if allowed_file(filename):
            filepath = os.path.join(image_folder, filename)
            date_taken = get_image_date_taken(filepath)
            if date_taken:
                print(f"\n{filename}")
                print("Choose category:")
                print("1: Phragmites")
                print("2: Narrowleaf Cattail")
                print("3: Yellow Iris")
                choice = input("Enter the number of the category: ")

                if choice == '1':
                    move_image(filename, 'phragmites', date_taken)
                elif choice == '2':
                    move_image(filename, 'narrowleaf_cattail', date_taken)
                elif choice == '3':
                    move_image(filename, 'yellow_iris', date_taken)
                else:
                    print("Invalid choice. Skipping this image.")

if __name__ == "__main__":
    categorize_images()
