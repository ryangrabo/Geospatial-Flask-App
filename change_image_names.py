import os
import json

COUNT_FILE = "image_count.json"

def load_counts():
    if os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_counts(counts):
    with open(COUNT_FILE, 'w') as f:
        json.dump(counts, f)

def rename_images(base_path):
    counts = load_counts()
    for plant_type in os.listdir(base_path):
        plant_path = os.path.join(base_path, plant_type)
        if os.path.isdir(plant_path):
            for date_folder in os.listdir(plant_path):
                date_path = os.path.join(plant_path, date_folder)
                if os.path.isdir(date_path):
                    day, month, year = date_folder.split('-')
                    images = [f for f in os.listdir(date_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                    if plant_type not in counts:
                        counts[plant_type] = 0
                    for image in images:
                        counts[plant_type] += 1
                        new_name = f"{plant_type}-{day}-{month}-{year}-{counts[plant_type]}{os.path.splitext(image)[1]}"
                        old_path = os.path.join(date_path, image)
                        new_path = os.path.join(date_path, new_name)
                        os.rename(old_path, new_path)
                        print(f"Renamed: {old_path} to {new_path}")
    save_counts(counts)

if __name__ == "__main__":
    base_path = "app/static/images" 
    rename_images(base_path)