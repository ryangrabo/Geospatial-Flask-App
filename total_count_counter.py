import os

def count_jpg_files(directory):
    """
    Walk through the given directory and count all .jpg files.
    Returns a dictionary with folder names as keys and their respective .jpg counts as values.
    Also returns the total count of .jpg files across all directories.
    """
    jpg_counts = {}
    total_jpg_count = 0
    phragmites_count = 0
    narrowleaf_cattail_count = 0
    purple_loosestrife_count = 0
    uncategorized_count = 0

    for root, dirs, files in os.walk(directory):
        relative_path = os.path.relpath(root, directory)  # Get relative path from the main directory
        jpg_count = sum(1 for file in files if file.lower().endswith('.jpg'))
        jpg_counts[relative_path] = jpg_count

        # Normalize the directory name for comparison
        normalized_path = relative_path.lower()

        if "phragmites" in normalized_path:
            phragmites_count += jpg_count
        elif "narrowleaf_cattail" in normalized_path:
            narrowleaf_cattail_count += jpg_count
        elif "purple_loosestrife" in normalized_path:
            purple_loosestrife_count += jpg_count
        else:
            uncategorized_count += jpg_count
        
        total_jpg_count += jpg_count

    return jpg_counts, total_jpg_count, phragmites_count, narrowleaf_cattail_count, purple_loosestrife_count, uncategorized_count

def write_counts_to_file(directory, counts, total, phragmites_total, narrowleaf_total, purple_total, uncategorized_total):
    """
    Writes the count of .jpg files for each folder to a text file.
    The file is named 'jpg_count.txt' and saved in the given directory.
    Includes the total count of .jpg files at the end.
    """
    output_file = os.path.join(directory, "jpg_count.txt")

    with open(output_file, 'w') as f:
        for folder, count in counts.items():
            indent_level = folder.count(os.sep)  # Determine the level of indentation
            indent = ' ' * (indent_level * 4)  # Indent based on the directory depth
            f.write(f"{indent}{folder}: {count} .jpg files\n")

        # Add the specific category totals
        f.write(f"\nPhragmites total: {phragmites_total} .jpg files\n")
        f.write(f"narrowleaf_cattail total: {narrowleaf_total} .jpg files\n")
        f.write(f"purple_loosestrife total: {purple_total} .jpg files\n")
        f.write(f"Uncategorized total: {uncategorized_total} .jpg files\n")

        # Add the full total count at the end
        f.write(f"\nTotal .jpg files: {total}\n")

    print(f"Counts and totals written to {output_file}")

if __name__ == "__main__":
    # Main directory path
    main_directory = r"C:\Users\rxg5517\OneDrive - The Pennsylvania State University\DRONES ONLY"

    if os.path.isdir(main_directory):
        jpg_counts, total_jpg_count, phragmites_count, narrowleaf_cattail_count, purple_loosestrife_count, uncategorized_count = count_jpg_files(main_directory)
        write_counts_to_file(main_directory, jpg_counts, total_jpg_count, phragmites_count, narrowleaf_cattail_count, purple_loosestrife_count, uncategorized_count)
    else:
        print("The provided directory does not exist.")
