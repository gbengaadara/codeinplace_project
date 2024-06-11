from tkinter import *
from PIL import Image, ImageTk

w = Tk()
w.geometry("400x600")

# Load your image (e.g., example_1.png)
img_open = Image.open("images/background.png")
img = ImageTk.PhotoImage(img_open)

# Create a label for the background image
background_label = Label(w, image=img)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

frame = LabelFrame(w, text="This is my frame")
frame.place(anchor="nw")
frame.pack()

b = Button(frame, text="Dont Click")
b.pack()
# Add other widgets to the LabelFrame as needed

w.mainloop()
