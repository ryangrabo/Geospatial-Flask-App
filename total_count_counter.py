import os

def count_and_size_jpg_files(directory):
    """
    Walk through the given directory and count all .jpg files.
    Returns a dictionary with folder names as keys and their respective .jpg counts and sizes as values.
    Also returns the total count and size of .jpg files across all directories.
    """
    jpg_counts = {}
    total_jpg_count = 0
    total_jpg_size = 0

    phragmites_count = 0
    phragmites_size = 0

    narrowleaf_cattail_count = 0
    narrowleaf_cattail_size = 0

    purple_loosetrife_count = 0
    purple_loosetrife_size = 0

    uncategorized_count = 0
    uncategorized_size = 0

    for root, dirs, files in os.walk(directory):
        relative_path = os.path.relpath(root, directory)  # Get relative path from the main directory
        jpg_count = 0
        jpg_size = 0

        for file in files:
            if file.lower().endswith('.jpg'):
                jpg_count += 1
                jpg_size += os.path.getsize(os.path.join(root, file))

        jpg_counts[relative_path] = (jpg_count, jpg_size)

        # Aggregate sizes and counts by category
        if "phragmites" in relative_path.lower():
            phragmites_count += jpg_count
            phragmites_size += jpg_size
        elif "narrowleaf_cattail" in relative_path.lower():
            narrowleaf_cattail_count += jpg_count
            narrowleaf_cattail_size += jpg_size
        elif "purple_loosetrife" in relative_path.lower():
            purple_loosetrife_count += jpg_count
            purple_loosetrife_size += jpg_size
        else:
            uncategorized_count += jpg_count
            uncategorized_size += jpg_size

        total_jpg_count += jpg_count
        total_jpg_size += jpg_size

    return (jpg_counts, total_jpg_count, total_jpg_size,
            phragmites_count, phragmites_size,
            narrowleaf_cattail_count, narrowleaf_cattail_size,
            purple_loosetrife_count, purple_loosetrife_size,
            uncategorized_count, uncategorized_size)

def format_size(size_in_bytes):
    """
    Formats the size from bytes to a human-readable format (KB, MB, GB).
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024

def write_counts_and_sizes_to_file(directory, counts, totals):
    """
    Writes the count and size of .jpg files for each folder to a text file.
    The file is named 'jpg_count.txt' and saved in the given directory.
    Includes the total count and size of .jpg files at the end.
    """
    output_file = os.path.join(directory, "jpg_count.txt")

    with open(output_file, 'w') as f:
        for folder, (count, size) in counts.items():
            indent_level = folder.count(os.sep)  # Determine the level of indentation
            indent = ' ' * (indent_level * 4)  # Indent based on the directory depth
            f.write(f"{indent}{folder}: {count} .jpg files, {format_size(size)}\n")

        # Add the specific category totals
        f.write(f"\nPhragmites total: {totals[3]} .jpg files, {format_size(totals[4])}\n")
        f.write(f"narrowleaf_cattail total: {totals[5]} .jpg files, {format_size(totals[6])}\n")
        f.write(f"purple_loosetrife total: {totals[7]} .jpg files, {format_size(totals[8])}\n")
        f.write(f"Uncategorized total: {totals[9]} .jpg files, {format_size(totals[10])}\n")

        # Add the full total count at the end
        f.write(f"\nTotal .jpg files: {totals[1]}, {format_size(totals[2])}\n")

    print(f"Counts and totals written to {output_file}")

if __name__ == "__main__":
    # Main directory path
    main_directory = r"C:\Users\rxg5517\OneDrive - The Pennsylvania State University\DRONES ONLY"

    if os.path.isdir(main_directory):
        totals = count_and_size_jpg_files(main_directory)
        write_counts_and_sizes_to_file(main_directory, *totals)
    else:
        print("The provided directory does not exist.")
