import os
from tkinter import Tk, Button, Canvas, Scrollbar, HORIZONTAL, VERTICAL, LEFT, RIGHT, BOTTOM, Frame, Label
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, root):

        self.check_image = ImageTk.PhotoImage(Image.open("check.png"))

        self.root = root
        self.root.title("Image Viewer")
        self.width = int(root.winfo_screenwidth() * 0.8)
        self.height = int(root.winfo_screenheight() * 0.8)
        self.root.geometry("{0}x{1}".format(self.width, self.height))
        self.root.resizable(width=False, height=False)

        self.top_frame = Frame(self.root)
        self.top_frame.pack(side="top", fill="x")

        font = ("Helvetica", 16, "bold")
        
        self.load_button = Button(self.top_frame, font=font, text="Cargar carpeta", command=self.load_directory,
                                  width=20)
        self.load_button.pack(side="top")

        self.center_frame = Frame(self.root)
        self.center_frame.pack(fill="both", expand=True)

        self.image_canvas = Canvas(self.center_frame)
        self.image_canvas.pack(side="top", fill="both", expand=True)

        self.bottom_frame = Frame(self.root)
        self.bottom_frame.pack(side="top", fill="x")

        self.select_button = Button(self.bottom_frame, font=font, text="Seleccionar Imagen", command=self.select_image, width=20, )
        self.select_button.pack(side="top")

        self.prev_button = Button(self.bottom_frame, font=font, text="Anterior", command=self.show_previous_image, width=20)
        self.prev_button.pack(side="top")

        self.next_button = Button(self.bottom_frame, font=font, text="Siguiente", command=self.show_next_image, width=20)
        self.next_button.pack(side="top")

        self.images = []
        self.selected_images = []

        self.current_image = 0
        self.image_label = Label(self.image_canvas)

    def load_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.images = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            self.current_image = 0
            self.show_image()

    def show_image(self):
        if self.images:
            image_path = self.images[self.current_image]
            image = Image.open(image_path)

            print(self.selected_images)

            if self.current_image not in self.selected_images:
                self.select_button.config(state="active")
            else:
                self.select_button.config(state="disabled")
    
            max_width = int(self.width * 0.8)
            max_height = int(self.height * 0.8)

            width, height = image.size
            if width > max_width or height > max_height:
                ratio = min(max_width / width, max_height / height)
                width = int(width * ratio)
                height = int(height * ratio)

            tk_image = ImageTk.PhotoImage(image.resize((width, height)))
            
            self.image_canvas.config(width=tk_image.width(), height=tk_image.height())
            self.image_canvas.create_image((self.width - tk_image.width()) // 2,
                                    (self.height - tk_image.height()) // 2, anchor="nw", image=tk_image)
            self.image_canvas.config(scrollregion=self.image_canvas.bbox("all"))

            self.image_label.configure(image=tk_image)
            self.image_label.image = tk_image

    def show_previous_image(self):
        if self.current_image > 0:
            self.current_image -= 1
            self.show_image()

    def show_next_image(self):
        if self.current_image < len(self.images) - 1:
            self.current_image += 1
            self.show_image()

    def select_image(self):
        if self.current_image not in self.selected_images:
            self.selected_images.append(self.current_image)
            self.select_button.config(state="disabled")

if __name__ == "__main__":
    root = Tk()
    viewer = ImageViewer(root)
    root.mainloop()
        