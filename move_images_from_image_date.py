import os
import shutil
import exifread
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools
from datetime import datetime

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'tif', 'tiff'}

def get_create_date(filepath):
    """
    Extracts the creation date from the image metadata using exifread.
    Tries multiple date tags in order.
    """
    with open(filepath, 'rb') as f:
        tags = exifread.process_file(f)
        for tag in ['EXIF DateTimeOriginal', 'EXIF DateTimeDigitized', 'Image DateTime']:
            if tag in tags:
                date_str = str(tags[tag])
                try:
                    # Handle the date format in the metadata
                    date_obj = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                    return date_obj
                except ValueError:
                    continue
    return None

def process_image(filepath, base_dir):
    """
    Processes a single image and moves it to a directory based on its creation date.
    """
    create_date = get_create_date(filepath)
    if create_date:
        # Format the folder name as 'month-day-year'
        folder_name = create_date.strftime('%m-%d-%Y')
        target_dir = os.path.join(base_dir, folder_name)
        os.makedirs(target_dir, exist_ok=True)
        filename = os.path.basename(filepath)
        target_path = os.path.join(target_dir, filename)
        shutil.move(filepath, target_path)
        print(f"Moved {filename} to {target_dir}")
    else:
        print(f"No valid date found for {os.path.basename(filepath)}. Skipping.")

def move_images_based_on_date(source_dir, batch_size=10, max_workers=4):
    """
    Moves images from source directory to date-based directories using multithreading.
    """
    image_files = [
        os.path.join(source_dir, f) for f in os.listdir(source_dir)
        if os.path.isfile(os.path.join(source_dir, f)) and f.lower().split('.')[-1] in ALLOWED_EXTENSIONS
    ]
    
    if not image_files:
        print("No image files found in the source directory.")
        return
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_image, filepath, source_dir) for filepath in image_files]
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    unprocessed_images_dir = r'C:\Users\rxg5517\OneDrive - The Pennsylvania State University\DRONES ONLY\unprocessed_images'
    phragmites_dir = r'C:\Users\rxg5517\OneDrive - The Pennsylvania State University\DRONES ONLY\phragmites'
    narrowleaf_cattail_dir = r'C:\Users\rxg5517\OneDrive - The Pennsylvania State University\DRONES ONLY\narrowleaf_cattail'
    purple_loosestrife_dir = r'C:\Users\rxg5517\OneDrive - The Pennsylvania State University\DRONES ONLY\purple_loosestrife'
    move_images_based_on_date(unprocessed_images_dir)
    move_images_based_on_date(phragmites_dir)
    move_images_based_on_date(narrowleaf_cattail_dir)
    move_images_based_on_date(purple_loosestrife_dir)
