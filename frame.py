from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import time

# Global variables for canvas size
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 600



# set up the canvas
root = Tk()
root.title("Code In Place - Frame")
geom = str(CANVAS_WIDTH) + "x" + str(CANVAS_HEIGHT)  # Make the string "400x600"
root.geometry(geom)
# background image
# my_canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
# my_canvas.pack(fill="both", expand=False)
my_image = ImageTk.PhotoImage(Image.open("images/background.png"))
# my_canvas.create_image(0, 0, image=bg, anchor="nw")



frame = LabelFrame(root, text="This is my frame", background=my_image)
frame.pack()


#dfdfd = LabelFrame()
b = Button(frame, text="Dont Click")
b.pack()

# my_canvas.mainloop()
root.mainloop()