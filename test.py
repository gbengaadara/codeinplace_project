from tkinter import *
from PIL import Image, ImageTk

root = Tk()
make_frame = LabelFrame(root, text="Sample Image", width=400, height=600)
make_frame.pack()

stim_filename = "images/background.png"
PIL_image = Image.open(stim_filename)
width, height = 400, 600
PIL_image_small = PIL_image.resize((width, height), Image.ANTIALIAS)

img = ImageTk.PhotoImage(PIL_image_small)
in_frame = Label(make_frame, image=img).pack
b = Button(in_frame, text="Dont Click").pack



root.mainloop()
