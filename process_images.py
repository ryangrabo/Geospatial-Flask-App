# Importing necessary libraries
import os           # Provides functions for interacting with the operating system
import shutil       # Offers a high-level interface for file operations
import subprocess   # Allows running of shell commands and interacting with system processes
import json         # Provides functions for parsing JSON data

def get_camera_orientation_pitch(filepath):
    """
    Extracts the camera orientation pitch from the EXIF metadata of an image using exiftool.

    Parameters:
    filepath (str): The path to the image file.

    Returns:
    float: The pitch value if found, otherwise None.
    """
    # Command to run exiftool.
    # Ensure exiftool.exe is installed and update the hard-coded path as needed.
    command = [
        'C:/../../../../geospatial-flask-app/exiftool.exe', #not sure if it works with relative path like this
        '-json',  # Output metadata in JSON format
        '-CameraOrientationNEDPitch',  # Specific tag to extract
        filepath  # File to process
    ]
    # Run the exiftool command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)
    # Check if the command was successful
    if result.returncode == 0:
        metadata = json.loads(result.stdout)  # Parse JSON output
        if metadata and 'CameraOrientationNEDPitch' in metadata[0]:
            return float(metadata[0]['CameraOrientationNEDPitch'])
    return None  # Return None if pitch data is not found

def move_images_based_on_pitch(source_dir, range_40_50_dir, range_55_65_dir):
    """
    Moves images to different directories based on their camera orientation pitch.

    Parameters:
    source_dir (str): The source directory containing the images.
    range_40_50_dir (str): The target directory for images with pitch between -50 and -40 degrees.
    range_55_65_dir (str): The target directory for images with pitch between -65 and -55 degrees.
    """
    for filename in os.listdir(source_dir):  # Iterate through files in the source directory
        if filename.endswith('.JPG'):                       # Process only JPEG files
            filepath = os.path.join(source_dir, filename)   # Construct the full file path
            pitch = get_camera_orientation_pitch(filepath)  # Get the pitch value
            if pitch is not None:                           # If pitch data is available
                print(f"Image: {filename}, Pitch: {pitch}")
                if -50 <= pitch <= -40:
                    # Move the file if pitch is between -50 and -40
                    shutil.move(filepath, os.path.join(range_40_50_dir, filename))
                    print(f"Moved {filename} to {range_40_50_dir}")
                elif -65 <= pitch <= -55:
                    # Move the file if pitch is between -65 and -55
                    shutil.move(filepath, os.path.join(range_55_65_dir, filename))
                    print(f"Moved {filename} to {range_55_65_dir}")
            else:
                print(f"No pitch data for {filename}")

if __name__ == "__main__":
    # Define the directories (update the hard-coded paths as needed)
    source_dir = r'C:\..\..\..\..\geospatial-flask-app\app\static\images'
    range_40_50_dir = r'C:\..\..\..\..\geospatial-flask-app\app\static\images\range_40_50'
    range_55_65_dir = r'C:\..\..\..\..\geospatial-flask-app\app\static\images\range_55_65'
    
    # Call the function to move images based on their pitch
    move_images_based_on_pitch(source_dir, range_40_50_dir, range_55_65_dir)
