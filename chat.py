from tkinter import *
from PIL import ImageTk, Image
import time

def main():
    root = Tk()
    root.geometry("400x600")

    # Load your background image
    background_image = Image.open("images/background.png")
    background_photo = ImageTk.PhotoImage(background_image)

    # Create a canvas to place the background image
    canvas = Canvas(root, width=600, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=background_photo)

    # Create a LabelFrame with no border and background matching the canvas
    label_frame = LabelFrame(canvas, text="", bg="white", bd=0)
    label_frame.pack(padx=20, pady=20)

    # Place the LabelFrame on the canvas
    canvas.create_window(100, 350, anchor="nw", window=label_frame)

    # Add a widget to the LabelFrame to demonstrate transparency
    label = Label(label_frame, text="This is a label inside LabelFrame", bg="white")
    label.pack(padx=10, pady=10)

    button_one = Button(label_frame, text="Add Equipment", width=30)
    button_one.pack(padx=10, pady=10)

    # Keep the window running
    root.mainloop()

def main_screen_buttons(root, my_canvas):
    # setup the buttons
    add_button = Button(root, text="Add Equipment", width=30)
    checkin_button = Button(root, text="Check In Equipment", width=30)
    checkout_button = Button(root, text="Check Out Equipment", width=30)
    exit_button = Button(root, text="Exit", width=30, command=root.quit)

    # add buttons
    one = my_canvas.create_window(100, 400, anchor="nw", window=add_button)
    two = my_canvas.create_window(100, 450, anchor="nw", window=checkin_button)
    three = my_canvas.create_window(100, 500, anchor="nw", window=checkout_button)
    four = my_canvas.create_window(100, 550, anchor="nw", window=exit_button)
    allwin = [one, two, three, four]
    return allwin



if __name__ == "__main__":
    main()
