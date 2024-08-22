import os
import shutil
from tkinter import Tk, Button, Label, Entry, Text, filedialog, messagebox, PhotoImage
from PIL import Image, ImageTk

class ImageMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Mover")
        self.source_directory = ""
        self.image_files = []
        self.current_image_index = 0
        
        self.picture_label = Label(self.root)
        self.picture_label.grid(row=0, column=1, columnspan=3)

        self.select_image_dir_button = Button(root, text="Choose Image Directory", command=self.select_image_directory)
        self.select_image_dir_button.grid(row=1, column=1)
        
        self.select_dest1_button = Button(root, text="Choose Phragmite folder", command=lambda: self.select_destination(1))
        self.select_dest1_button.grid(row=2, column=1)
        
        self.select_dest2_button = Button(root, text="Choose Cattail folder", command=lambda: self.select_destination(2))
        self.select_dest2_button.grid(row=3, column=1)
        
        self.select_dest3_button = Button(root, text="Choose Purple Loosetrife", command=lambda: self.select_destination(3))
        self.select_dest3_button.grid(row=4, column=1)
        
        self.dest1_label = Label(root, text="Phragmite:")
        self.dest1_label.grid(row=2, column=2)
        
        self.dest1_entry = Entry(root, width=50)
        self.dest1_entry.grid(row=2, column=3)
        
        self.dest2_label = Label(root, text="Cattail:")
        self.dest2_label.grid(row=3, column=2)
        
        self.dest2_entry = Entry(root, width=50)
        self.dest2_entry.grid(row=3, column=3)
        
        self.dest3_label = Label(root, text="Purple Loosetrife:")
        self.dest3_label.grid(row=4, column=2)
        
        self.dest3_entry = Entry(root, width=50)
        self.dest3_entry.grid(row=4, column=3)

        self.move_to_dest1_button = Button(root, text="Move to Destination 1", command=lambda: self.move_image(1))
        self.move_to_dest1_button.grid(row=2, column=4)

        self.move_to_dest2_button = Button(root, text="Move to Destination 2", command=lambda: self.move_image(2))
        self.move_to_dest2_button.grid(row=3, column=4)

        self.move_to_dest3_button = Button(root, text="Move to Destination 3", command=lambda: self.move_image(3))
        self.move_to_dest3_button.grid(row=4, column=4)
        
        self.delete_button = Button(root, text="Delete Current Image", command=self.delete_current_image, bg="red", fg="white")
        self.delete_button.grid(row=5, column=2)

        self.log_text = Text(root, height=10, width=80)
        self.log_text.grid(row=6, column=1, columnspan=4)

    def log_message(self, message):
        self.log_text.insert('end', message + "\n")
        self.log_text.see('end')

    def select_image_directory(self):
        self.source_directory = filedialog.askdirectory()
        if self.source_directory:
            self.image_files = [f for f in os.listdir(self.source_directory) if f.endswith('.jpg')]
            self.current_image_index = 0
            self.show_image()
            self.log_message(f"Selected directory: {self.source_directory}")

    def select_destination(self, dest_number):
        destination = filedialog.askdirectory()
        if destination:
            if dest_number == 1:
                self.dest1_entry.delete(0, 'end')
                self.dest1_entry.insert(0, destination)
            elif dest_number == 2:
                self.dest2_entry.delete(0, 'end')
                self.dest2_entry.insert(0, destination)
            elif dest_number == 3:
                self.dest3_entry.delete(0, 'end')
                self.dest3_entry.insert(0, destination)
            self.log_message(f"Selected destination {dest_number}: {destination}")

    def show_image(self):
        if self.image_files:
            img_path = os.path.join(self.source_directory, self.image_files[self.current_image_index])
            img = Image.open(img_path)
            img.thumbnail((300, 300))
            img = ImageTk.PhotoImage(img)
            self.picture_label.config(image=img)
            self.picture_label.image = img
            self.log_message(f"Displaying {os.path.basename(img_path)}")
        else:
            self.log_message("No images found in the selected directory.")

    def move_image(self, dest_number):
        if not self.image_files:
            self.log_message("No image to move.")
            return

        if dest_number == 1:
            destination_directory = self.dest1_entry.get()
        elif dest_number == 2:
            destination_directory = self.dest2_entry.get()
        elif dest_number == 3:
            destination_directory = self.dest3_entry.get()

        if not destination_directory:
            self.log_message("Destination not selected. Please choose a destination directory.")
            return

        current_image = self.image_files[self.current_image_index]
        source_path = os.path.join(self.source_directory, current_image)
        destination_path = os.path.join(destination_directory, current_image)

        try:
            shutil.move(source_path, destination_path)
            self.log_message(f"Moved {current_image} to {destination_directory}")
            self.current_image_index += 1
            if self.current_image_index < len(self.image_files):
                self.show_image()
            else:
                self.log_message("No more images to move.")
                self.picture_label.config(image='')
        except Exception as ex:
            self.log_message(f"Error moving file: {str(ex)}")

    def delete_current_image(self):
        if not self.image_files:
            self.log_message("No image to delete.")
            return

        current_image = self.image_files[self.current_image_index]
        image_path = os.path.join(self.source_directory, current_image)

        try:
            os.remove(image_path)
            self.log_message(f"Deleted {current_image}")
            self.current_image_index += 1
            if self.current_image_index < len(self.image_files):
                self.show_image()
            else:
                self.log_message("No more images to display.")
                self.picture_label.config(image='')
        except Exception as ex:
            self.log_message(f"Error deleting file: {str(ex)}")

if __name__ == "__main__":
    root = Tk()
    app = ImageMoverApp(root)
    root.mainloop()
