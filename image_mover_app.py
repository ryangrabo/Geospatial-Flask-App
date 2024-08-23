import os
import shutil
from tkinter import Tk, Button, Label, Entry, Text, filedialog, Frame
from PIL import Image, ImageTk

class ImageMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Mover")
        self.root.geometry("800x600")
        self.source_directory = "C:/Users/rxg5517/OneDrive - The Pennsylvania State University/DRONES ONLY/unprocessed_images"
        self.image_files = []
        self.current_image_index = 0
        self.current_image = None

        # Default destination directories
        self.default_destinations = [
            "C:/Users/rxg5517/OneDrive - The Pennsylvania State University/DRONES ONLY/phragmites",
            "C:/Users/rxg5517/OneDrive - The Pennsylvania State University/DRONES ONLY/narrowleaf_cattail",
            "C:/Users/rxg5517/OneDrive - The Pennsylvania State University/DRONES ONLY/purple_loosestrife"
        ]

        self.setup_ui()
        self.load_images()
        self.root.update()  # Force an update of the window
        self.root.after(100, self.update_image)  # Schedule image update after a short delay

    def setup_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        main_frame = Frame(self.root, bg="#f0f0f0")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        left_frame = Frame(main_frame, bg="#f0f0f0")
        left_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10))

        right_frame = Frame(main_frame, bg="#f0f0f0")
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Image display
        self.image_frame = Frame(right_frame, bg="white", width=500, height=400)
        self.image_frame.grid(row=0, column=0, sticky="nsew")
        self.image_frame.grid_propagate(False)

        self.picture_label = Label(self.image_frame, bg="white")
        self.picture_label.place(relx=0.5, rely=0.5, anchor="center")

        # Buttons
        button_style = {"font": ("Arial", 10), "bg": "#4CAF50", "fg": "white", "padx": 10, "pady": 5}

        self.select_image_dir_button = Button(left_frame, text="Choose Image Directory", command=self.select_image_directory, **button_style)
        self.select_image_dir_button.pack(fill="x", pady=(0, 10))

        for i, text in enumerate(["Phragmite", "Cattail", "Purple Loosetrife"]):
            setattr(self, f"select_dest{i+1}_button", Button(left_frame, text=f"Choose {text} folder", command=lambda i=i: self.select_destination(i+1), **button_style))
            getattr(self, f"select_dest{i+1}_button").pack(fill="x", pady=(0, 5))

        # Destination entries with default paths
        for i, text in enumerate(["Phragmite", "Cattail", "Purple Loosestrife"]):
            frame = Frame(right_frame, bg="#f0f0f0")
            frame.grid(row=i+1, column=0, sticky="ew", pady=(0, 5))
            
            Label(frame, text=f"{text}:", bg="#f0f0f0", font=("Arial", 10)).pack(side="left", padx=(0, 5))
            entry = Entry(frame, font=("Arial", 10))
            entry.insert(0, self.default_destinations[i])  # Set default destination
            entry.pack(side="left", expand=True, fill="x")
            setattr(self, f"dest{i+1}_entry", entry)

            Button(frame, text=f"Move to {text}", command=lambda i=i: self.move_image(i+1), **button_style).pack(side="right", padx=(5, 0))

        # Delete button
        self.delete_button = Button(right_frame, text="Delete Current Image", command=self.delete_current_image, font=("Arial", 10), bg="red", fg="white", padx=10, pady=5)
        self.delete_button.grid(row=4, column=0, sticky="ew", pady=(10, 0))

        # Log
        self.log_text = Text(main_frame, height=5, font=("Arial", 10))
        self.log_text.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))

    def load_images(self):
        if self.source_directory:
            self.image_files = [f for f in os.listdir(self.source_directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            self.current_image_index = 0
            self.show_image()
            self.log_message(f"Selected directory: {self.source_directory}")
            self.log_message(f"Found {len(self.image_files)} images in the directory.")

    def show_image(self):
        if self.image_files:
            img_path = os.path.join(self.source_directory, self.image_files[self.current_image_index])
            self.current_image = Image.open(img_path)
            self.update_image()
            self.log_message(f"Displaying {os.path.basename(img_path)}")
        else:
            self.log_message("No images found in the selected directory.")

    def update_image(self):
        if self.current_image:
            # Get the current frame dimensions
            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()

            # Check if frame dimensions are valid
            if frame_width <= 1 or frame_height <= 1:
                # Frame not properly sized yet, schedule an update for later
                self.root.after(100, self.update_image)
                return

            # Calculate the scaling factor to fit the image in the frame
            frame_ratio = frame_width / frame_height
            img_ratio = self.current_image.width / self.current_image.height
            
            if img_ratio > frame_ratio:
                new_width = frame_width
                new_height = int(new_width / img_ratio)
            else:
                new_height = frame_height
                new_width = int(new_height * img_ratio)

            img_resized = self.current_image.copy()
            img_resized.thumbnail((new_width, new_height), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_resized)
            
            self.picture_label.config(image=img_tk)
            self.picture_label.image = img_tk

    def select_image_directory(self):
        self.source_directory = filedialog.askdirectory()
        self.load_images()

    def select_destination(self, dest_number):
        destination = filedialog.askdirectory()
        if destination:
            getattr(self, f"dest{dest_number}_entry").delete(0, 'end')
            getattr(self, f"dest{dest_number}_entry").insert(0, destination)
            self.log_message(f"Selected destination {dest_number}: {destination}")

    def move_image(self, dest_number):
        if not self.image_files:
            self.log_message("No image to move.")
            return

        destination_directory = getattr(self, f"dest{dest_number}_entry").get()

        if not destination_directory:
            self.log_message("Destination not selected. Please choose a destination directory.")
            return

        current_image = self.image_files[self.current_image_index]
        source_path = os.path.join(self.source_directory, current_image)
        destination_path = os.path.join(destination_directory, current_image)

        try:
            shutil.move(source_path, destination_path)
            self.log_message(f"Moved {current_image} to {destination_directory}")
            self.image_files.pop(self.current_image_index)
            if self.image_files:
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
            self.image_files.pop(self.current_image_index)
            if self.image_files:
                self.show_image()
            else:
                self.log_message("No more images to display.")
                self.picture_label.config(image='')
        except Exception as ex:
            self.log_message(f"Error deleting file: {str(ex)}")

    def log_message(self, message):
        self.log_text.insert('end', message + "\n")
        self.log_text.see('end')

if __name__ == "__main__":
    root = Tk()
    app = ImageMoverApp(root)
    root.mainloop()
