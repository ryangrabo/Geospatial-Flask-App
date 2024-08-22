import os           # Provides functions for interacting with the operating system
import shutil       # Offers a high-level interface for file operations
import subprocess   # Allows running of shell commands and interacting with system processes
import json         # Provides functions for parsing JSON data
from concurrent.futures import ThreadPoolExecutor, as_completed  # Provides functions for parallel processing
import itertools    # Provides functions to create iterators for efficient looping

def get_camera_orientation_pitch(filepath):
    """
    Extracts the camera orientation pitch from the EXIF metadata of an image using exiftool.

    Parameters:
    filepath (str): The path to the image file.

    Returns:
    float: The pitch value if found, otherwise None.
    """
    command = [
        'exiftool.exe',  # not sure if it works with relative path like this
        '-json',  # Output metadata in JSON format
        '-CameraOrientationNEDPitch',  # Specific tag to extract
        filepath  # File to process
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        metadata = json.loads(result.stdout)  # Parse JSON output
        if metadata and 'CameraOrientationNEDPitch' in metadata[0]:
            return float(metadata[0]['CameraOrientationNEDPitch'])
    return None  # Return None if pitch data is not found

def process_image(filepath, range_44_46, range_not_44_46):
    """
    Processes a single image to move it to the correct directory based on its pitch.

    Parameters:
    filepath (str): The path to the image file.
    range_44_46 (str): The target directory for images with pitch between -44 and -46 degrees.
    range_not_44_46 (str): The target directory for images with pitch not between -44 and -46 degrees.
    """
    pitch = get_camera_orientation_pitch(filepath)  # Get the pitch value
    if pitch is not None:                           # If pitch data is available
        filename = os.path.basename(filepath)
        print(f"Image: {filename}, Pitch: {pitch}")
        if -47 <= pitch <= -43:
            shutil.move(filepath, os.path.join(range_44_46, filename))
            print(f"Moved {filename} to {range_44_46}")
        else:
            shutil.move(filepath, os.path.join(range_not_44_46, filename))
            print(f"Moved {filename} to {range_not_44_46}")
    else:
        print(f"No pitch data for {filename}")

def move_images_based_on_pitch(source_dir, range_44_46, range_not_44_46, batch_size=10, max_workers=4):
    """
    Moves images to different directories based on their camera orientation pitch using parallel processing.

    Parameters:
    source_dir (str): The source directory containing the images.
    range_44_46 (str): The target directory for images with pitch between -44 and -46 degrees.
    range_not_44_46 (str): The target directory for images with pitch not between -44 and -46 degrees.
    batch_size (int): The number of images to process in each batch.
    max_workers (int): The maximum number of threads to use for parallel processing.
    """
    image_files = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if f.endswith('.JPG')]
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for batch in batch_iterable(image_files, batch_size):
            futures = [executor.submit(process_image, filepath, range_44_46, range_not_44_46) for filepath in batch]
            for future in as_completed(futures):
                future.result()

def batch_iterable(iterable, batch_size):
    """
    Splits an iterable into batches of a specified size.

    Parameters:
    iterable (iterable): The iterable to split.
    batch_size (int): The size of each batch.

    Returns:
    generator: A generator that yields batches of the specified size.
    """
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, batch_size))
        if not batch:
            break
        yield batch

if __name__ == "__main__":
    # Define the directories (update the hard-coded paths as needed)
    source_dir = r'Filter_Images_Directory\Unfiltered_Images'
    range_44_46 = r'Filter_Images_Directory\range_44_46'
    range_not_44_46 = r'Filter_Images_Directory\range_not_44_46'
    
    # Call the function to move images based on their pitch
    move_images_based_on_pitch(source_dir, range_44_46, range_not_44_46)
