from tkinter import *
from PIL import ImageTk, Image
import time

# Global variables for canvas size
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 600

def main():

    # set up the canvas
    global f
    root = Tk()
    root.title("Code In Place - Equipment Logger")
    geom = str(CANVAS_WIDTH) + "x" + str(CANVAS_HEIGHT)  # Make the string "400x600"
    root.geometry(geom)
    my_canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    my_canvas.pack(fill="both", expand=False)

    # background image
    bg = ImageTk.PhotoImage(file="images/background.png")
    my_canvas.create_image(0, 0, image=bg, anchor="nw")

    main_screen_buttons(root, my_canvas)


    my_canvas.mainloop()

def main_screen_buttons(root, my_canvas):
    # setup the buttons
    add_button = Button(root, text="Add Equipment", width=30, command=ab_level)
    checkin_button = Button(root, text="Check In Equipment", width=30, command=ci_level)
    checkout_button = Button(root, text="Check Out Equipment", width=30, command=co_level)
    exit_button = Button(root, text="Exit", width=30, command=root.quit)

    # add buttons
    one = my_canvas.create_window(100, 400, anchor="nw", window=add_button)
    two = my_canvas.create_window(100, 450, anchor="nw", window=checkin_button)
    three = my_canvas.create_window(100, 500, anchor="nw", window=checkout_button)
    four = my_canvas.create_window(100, 550, anchor="nw", window=exit_button)
    allwin = [one, two, three, four]
    return allwin

def ab_level():
    ab = Toplevel()
    ab.title("Add Equipment")
    ab.geometry("400x400")
    un_entry = Entry(ab, font=("Helvetica", 24), width=14, fg="#336d92")
    un_entry.pack()
    def exit_btn():
        ab.destroy()
        ab.update()

    btn = Button(ab, text='EXIT', command=exit_btn)
    btn.pack()

def ci_level():
    ci = Toplevel()
    ci.title("Add Equipment")
    ci.geometry("400x400")
    un_entry = Entry(ci, font=("Helvetica", 24), width=14, fg="#336d92")
    un_entry.pack()
    def exit_btn():
        ci.destroy()
        ci.update()

    btn = Button(ci, text='EXIT', command=exit_btn)
    btn.pack()

def co_level():
    co = Toplevel()
    co.title("Add Equipment")
    co.geometry("400x400")
    un_entry = Entry(co, font=("Helvetica", 24), width=14, fg="#336d92")
    un_entry.pack()
    def exit_btn():
        co.destroy()
        co.update()

    btn = Button(co, text='EXIT', command=exit_btn)
    btn.pack()

# define entry box
# un_entry = Entry(root, font=("Helvetica", 24), width=14, fg="#336d92")

# Add the entry boxes

# un_window = my_canvas.create_window(100, 100, anchor="nw", window=un_entry)


#    left_x = CANVAS_WIDTH / 2 - (SQUARE_SIZE / 2)
#    top_y = CANVAS_HEIGHT / 2 - (SQUARE_SIZE / 2)
#    right_x = left_x + SQUARE_SIZE
#    bottom_y = top_y + SQUARE_SIZE

# rect = my_canvas.create_rectangle(left_x, top_y, right_x, bottom_y)
# time.sleep(6)


if __name__ == '__main__':
    main()