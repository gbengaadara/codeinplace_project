from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
from datetime import datetime
import time

# Global variables for canvas size
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 600
SUB_WINDOW_WIDTH = 300
SUB_WINDOW_HEIGHT = 250

def main():

    # set up the canvas
    root = Tk()
    root.title("Basic Equipment Logger")
    geom = str(CANVAS_WIDTH) + "x" + str(CANVAS_HEIGHT)  # Make the string "400x600"
    root.geometry(geom)
    my_canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    my_canvas.pack(fill="both", expand=False)

    # background image
    bg = ImageTk.PhotoImage(file="images/background.png")
    my_canvas.create_image(0, 0, image=bg, anchor="nw")

    main_screen_buttons(root, my_canvas)
    # create_table_equipment()
    # create_table_log()
    my_canvas.mainloop()

def focus_next(event):
    event.widget.tk_focusNext().focus_set()


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


# Create window and associated entry boxes, labels and buttons for equipment entry into database
def ab_level():
    ab = Toplevel()
    ab.title("Add Equipment")
    geom = str(SUB_WINDOW_WIDTH) + "x" + str(SUB_WINDOW_HEIGHT)  # Make the string for sub window
    ab.geometry(geom)

    # Create drop down for equipment typer
    e_type = StringVar()
    e_type.set("Scanner")
    drop = OptionMenu(ab, e_type,  "Scanner", "Printer")
    drop.config(width=15)
    drop.grid(row=1, column = 1, padx=5, pady=5)
    # e_type = Entry(ab, width=20) # entry box option
    # e_type.grid(row=1, column=1, padx=5, pady=5) # entry box option
    # Create Entry boxes for Type and Serial Number
    s_number = Entry(ab, width=20)
    s_number.focus()
    s_number.grid(row=2, column=1, padx=5, pady=5)

    # Create labels for drop down and entry box and window info
    intro_label = Label(ab, text="Equip. details")
    intro_label.grid(row=0, column=0, padx=5, pady=5)
    e_type_label = Label(ab, text="Equip. Type")
    e_type_label.grid(row=1, column=0, padx=5, pady=5)
    s_number_label = Label(ab, text="Serial Number")
    s_number_label.grid(row=2, column=0, padx=5, pady=5)


    # Exit and submit button functions
    def exit_btn():
        ab.destroy()
        ab.update()
    def submit_btn():
        # Enter values into database
        conn = sqlite3.connect("equipment.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO equipments (type, serial_number) VALUES (:e_type, :s_number)",
                       {
                           'e_type': e_type.get(),
                           's_number': s_number.get()
                       })
        # commit changes
        conn.commit()
        conn.close()
        # Get entered values for success message box
        e_type1 = e_type.get()
        s_num = s_number.get()
        # Success message
        message = "You successfully added " + e_type1 + " serial number " + s_num
        messagebox.showinfo("Information!", message, parent=ab)
        # Clear text boxes
        # e_type.delete(0, END) # needed if using entry box
        s_number.delete(0, END)


    # Submit and Exit buttons
    exit_btn = Button(ab, text='Exit', command=exit_btn)
    exit_btn.grid(row=4, column=0, columnspan=2, ipadx=110, padx=5, pady=5)
    submit_btn = Button(ab, text='Submit', command=submit_btn)
    submit_btn.grid(row=3, column=0, columnspan=2, ipadx=100, padx=5, pady=5)


# Create window and associated entry boxes, labels and buttons for equipment check out into database
def co_level():
    co = Toplevel()
    co.title("Check Out Equipment")
    geom = str(SUB_WINDOW_WIDTH) + "x" + str(SUB_WINDOW_HEIGHT)  # Make the string for sub window
    co.geometry(geom)
    # co.geometry("300x250")

    # Create Entry boxes for Type and Serial Number
    employee_id = Entry(co, width=20)
    employee_id.focus()
    employee_id.bind("<Return>", focus_next)  # Bind Enter key to focus_next function
    employee_id.grid(row=1, column=1, padx=5, pady=5)
    s_number = Entry(co, width=20)
    s_number.grid(row=2, column=1, padx=5, pady=5)

    # Create labels
    intro_label = Label(co, text="Check Out")
    intro_label.grid(row=0, column=0, padx=5, pady=5)
    employee_id_label = Label(co, text="Employee ID")
    employee_id_label.grid(row=1, column=0, padx=5, pady=5)
    s_number_label = Label(co, text="Serial Number")
    s_number_label.grid(row=2, column=0, padx=5, pady=5)
    #un_entry = Entry(ab, font=("Helvetica", 24), width=14, fg="#336d92")
    #un_entry.pack()

    # Exit and submit button functions
    def exit_btn():
        co.destroy()
        co.update()
    def submit_btn():
        # Get current date and time
        # now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        # print(now)

        # Get entered values for success message box
        employee_id1 = employee_id.get()
        s_num = s_number.get()
        conn = sqlite3.connect("equipment.db")
        cursor = conn.cursor()
        # Check if equipment already in database and exit with info if not
        cursor.execute("SELECT id FROM equipments WHERE serial_number = ?", (s_num,))
        data = cursor.fetchone()
        cursor.execute("SELECT count(serial_number) FROM check_out_log WHERE serial_number = ? AND time_in is null", (s_num,))
        data2 = cursor.fetchone()[0]
        # print(data2)
        if data is None:
            message = "Equipment serial number " + s_num + " is not in the database. Please add equipment first"
            messagebox.showinfo("Information!", message, parent=co)
            co.destroy()
            co.update()
        elif data2 == 1:
            message = "Equipment serial number " + s_num + " is already checked out. Please check it in first"
            messagebox.showinfo("Information!", message, parent=co)
            co.destroy()
            co.update()
        else:
            # Enter values into database
            cursor.execute("INSERT INTO check_out_log (employee_id, serial_number) VALUES (:employee_id, :s_number)",
                           {
                           'employee_id': employee_id.get(),
                           's_number': s_number.get()
                       })
            # commit changes
            conn.commit()
            conn.close()
            # print(employee_id, s_number)
            # Get entered values for success message box
            # employee_id1 = employee_id.get()
            # s_num = s_number.get()
            # Success message
            message = "Hello " + employee_id1 + " you checked out equipment serial number " + s_num
            messagebox.showinfo("Information!", message, parent=co)
            # Clear text boxes
            employee_id.delete(0, END)
            s_number.delete(0, END)



    # Submit and Exit buttons
    exit_btn = Button(co, text='Exit', command=exit_btn)
    exit_btn.grid(row=4, column=0, columnspan=2, ipadx=110, padx=5, pady=5)
    submit_btn = Button(co, text='Submit', command=submit_btn)
    submit_btn.grid(row=3, column=0, columnspan=2, ipadx=100, padx=5, pady=5)


# Create window and associated entry boxes, labels and buttons for equipment check in into database
def ci_level():
    ci = Toplevel()
    ci.title("Check In Equipment")
    geom = str(SUB_WINDOW_WIDTH) + "x" + str(SUB_WINDOW_HEIGHT)  # Make the string for sub window
    ci.geometry(geom)
    # ci.geometry("300x250")

    # Create Entry box for Serial Number
    s_number = Entry(ci, width=20)
    s_number.focus()
    s_number.grid(row=1, column=1, padx=5, pady=5)
    # Create drop down box for equipment status (Good or Bad)
    # e_status = Entry(ci, width=20)
    # e_status.grid(row=2, column=1, padx=5, pady=5)
    e_status = StringVar()
    e_status.set("Good")
    drop = OptionMenu(ci, e_status,  "Good", "Bad")
    drop.config(width=15)
    drop.grid(row=2, column = 1, padx=5, pady=5)




    # Create labels
    intro_label = Label(ci, text="Check In")
    intro_label.grid(row=0, column=0, padx=5, pady=5)
    s_number_label = Label(ci, text="Serial Number")
    s_number_label.grid(row=1, column=0, padx=5, pady=5)
    e_status_label = Label(ci, text="Status")
    e_status_label.grid(row=2, column=0, padx=5, pady=5)

    # Exit and submit button functions
    def exit_btn():
        ci.destroy()
        ci.update()
    def submit_btn():
        # Get current date and time
        now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print(now)

        # Get entered values for success message box
        e_status1 = e_status.get()
        s_num = s_number.get()
        conn = sqlite3.connect("equipment.db")
        cursor = conn.cursor()
        # Check if equipment already in database and exit with info if not
        cursor.execute("SELECT id FROM equipments WHERE serial_number = ?", (s_num,))
        data = cursor.fetchone()
        cursor.execute("SELECT count(serial_number) FROM check_out_log WHERE serial_number = ? AND time_in is null", (s_num,))
        data2 = cursor.fetchone()[0]
        # print(data2)
        if data is None:
            message = "Equipment serial number " + s_num + " is not in the database. Please add equipment first and check it out if needed"
            messagebox.showinfo("Information!", message, parent=ci)
            ci.destroy()
            ci.update()
        elif data2 == 0:
            message = "Equipment serial number " + s_num + " is not checked out. Please check it out first"
            messagebox.showinfo("Information!", message, parent=ci)
            ci.destroy()
            ci.update()
        else:
            # Enter values into database
            # UPDATE  table_name  SET   column1 = value1, column2 = value2   WHERE  condition;
            cursor.execute("UPDATE  check_out_log SET time_in = ?, status = ? where serial_number = ?",
                           (now, e_status1, s_num))
            # commit changes
            conn.commit()
            conn.close()
            # print(employee_id, s_number)
            # Get entered values for success message box
            # employee_id1 = employee_id.get()
            # s_num = s_number.get()
            # Success message
            message = "Hello, you checked in equipment serial number " + s_num
            messagebox.showinfo("Information!", message, parent=ci)
            # Clear text boxes
            e_status.delete(0, END)
            s_number.delete(0, END)



    # Submit and Exit buttons
    exit_btn = Button(ci, text='Exit', command=exit_btn)
    exit_btn.grid(row=4, column=0, columnspan=2, ipadx=110, padx=5, pady=5)
    submit_btn = Button(ci, text='Submit', command=submit_btn)
    submit_btn.grid(row=3, column=0, columnspan=2, ipadx=100, padx=5, pady=5)


def create_table_equipment():
    conn = sqlite3.connect("equipment.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE equipments(
    id INTEGER PRIMARY KEY,
    type text,
    serial_number text
    )""")

    #commit changes
    conn.commit()
    conn.close()

def create_table_log():
    conn = sqlite3.connect("equipment.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE check_out_log(
    id INTEGER PRIMARY KEY,
    employee_id text,
    serial_number text,
    timestamp_out DATETIME DEFAULT CURRENT_TIMESTAMP,
    time_in text,
    status text
    )""")

    #commit changes
    conn.commit()
    conn.close()





if __name__ == '__main__':
    main()