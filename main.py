from tkinter import *
from tkinter import messagebox
from PIL import ImageTk  # , Image
import sqlite3
from datetime import datetime
# import time

""" This is a basic equipment logger program created as a final project for 
Stanford University Code In Place 2024 by Olu A """

# Global variables for canvas and sub window size
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 600
SUB_WINDOW_WIDTH = 300
SUB_WINDOW_HEIGHT = 250


def main():
    # set up the main canvas window
    root = Tk()
    root.title("Basic Equipment Logger")
    geom = str(CANVAS_WIDTH) + "x" + str(CANVAS_HEIGHT)  # Make the string "400x600"
    root.geometry(geom)
    my_canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    my_canvas.pack(fill="both", expand=False)

    # set up background image. Image courtesy of www.freepik.com
    # (view-steel-hammer-with-other-construction-elements-tools.jpg)
    bg = ImageTk.PhotoImage(file="images/background.png")
    my_canvas.create_image(0, 0, image=bg, anchor="nw")

    # create a frame to hold the App title
    frame = LabelFrame(root, text="", bg="yellow", padx=5, pady=5, borderwidth=12)
    frame.place(x=80, y=50, anchor="nw")
    # App title
    text = Label(frame, text="Basic \n Equipment Logger App", bg="yellow", font=("helvetica", 15))
    text.grid(row=2, column=4)

    # the function to set up buttons on the home screen
    main_screen_buttons(root, my_canvas)

    # Create sqlite3 tables. Tables will only be created if not already existing
    create_table_equipment()
    create_table_log()

    my_canvas.mainloop()


# function to set focus to next widget on screen
def focus_next(event):
    event.widget.tk_focusNext().focus_set()

# creating the main screen buttons to call other windows


def main_screen_buttons(root, my_canvas):
    # set up the buttons
    add_button = Button(root, text="Add Equipment", width=30, command=ab_level)
    checkin_button = Button(root, text="Check In Equipment", width=30, command=ci_level)
    checkout_button = Button(root, text="Check Out Equipment", width=30, command=co_level)
    exit_button = Button(root, text="Exit", width=30, command=root.quit)
    query_eqp_button = Button(root, text="Equipment List", width=30, command=query_eqp)
    query_log_button = Button(root, text="Equipment Log", width=30, command=query_log)

    # add buttons
    my_canvas.create_window(100, 300, anchor="nw", window=add_button)
    my_canvas.create_window(100, 350, anchor="nw", window=checkin_button)
    my_canvas.create_window(100, 400, anchor="nw", window=checkout_button)
    my_canvas.create_window(100, 450, anchor="nw", window=query_eqp_button)
    my_canvas.create_window(100, 500, anchor="nw", window=query_log_button)
    my_canvas.create_window(100, 550, anchor="nw", window=exit_button)


# Create window and associated entry boxes, labels and buttons for equipment entry into database
def ab_level():
    ab = Toplevel()
    ab.title("Add Equipment")
    geom = str(SUB_WINDOW_WIDTH) + "x" + str(SUB_WINDOW_HEIGHT)  # Make the string for sub window
    ab.geometry(geom)

    # Create labels for drop down and entry box and window info
    intro_label = Label(ab, text="Equip. details")
    intro_label.grid(row=0, column=0, padx=5, pady=5)
    e_type_label = Label(ab, text="Equip. Type")
    e_type_label.grid(row=1, column=0, padx=5, pady=5)
    s_number_label = Label(ab, text="Serial Number")
    s_number_label.grid(row=2, column=0, padx=5, pady=5)

    # Create drop down for equipment type
    e_type = StringVar()
    e_type.set("Scanner")
    drop = OptionMenu(ab, e_type,  "Scanner", "Printer")
    drop.config(width=15)
    drop.grid(row=1, column=1, padx=5, pady=5)
    s_number = Entry(ab, width=20)
    s_number.focus()
    s_number.bind("<Return>", focus_next)  # Bind the Enter key to focus_next widget
    s_number.grid(row=2, column=1, padx=5, pady=5)

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
        s_number.delete(0, END)

    # Submit and Exit buttons
    submit_btn = Button(ab, text='Submit', command=submit_btn)
    submit_btn.grid(row=3, column=0, columnspan=2, ipadx=100, padx=5, pady=5)
    exit_btn = Button(ab, text='Close', command=exit_btn)
    exit_btn.grid(row=4, column=0, columnspan=2, ipadx=110, padx=5, pady=5)


# Create window and associated entry boxes, labels and buttons for equipment check out into database
def co_level():
    co = Toplevel()
    co.title("Check Out Equipment")
    geom = str(SUB_WINDOW_WIDTH) + "x" + str(SUB_WINDOW_HEIGHT)  # Make the string for sub window
    co.geometry(geom)

    # Create Entry boxes for Type and Serial Number
    employee_id = Entry(co, width=20)
    employee_id.focus()
    employee_id.bind("<Return>", focus_next)  # Bind the Enter key to focus_next widget
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
    #test_entry = Entry(ab, font=("Helvetica", 24), width=14, fg="#336d92") #testing
    #test_entry.pack()

    # Exit and submit button functions
    def exit_btn():
        co.destroy()
        co.update()

    def submit_btn():
        # Get entered values for success message box
        employee_id1 = employee_id.get()
        s_num = s_number.get()
        conn = sqlite3.connect("equipment.db")
        cursor = conn.cursor()
        # Check if equipment already in database and exit with information if not
        cursor.execute("SELECT id FROM equipments WHERE serial_number = ?", (s_num,))
        data = cursor.fetchone()
        cursor.execute("SELECT count(serial_number) FROM check_out_log WHERE serial_number = ? AND time_in is null",
                       (s_num,))
        data2 = cursor.fetchone()[0]
        # print(data2) #debugging
        # Message if equipment not in the database
        if data is None:
            message = "Equipment serial number " + s_num + " is not in the database. Please add equipment first"
            messagebox.showinfo("Information!", message, parent=co)
            co.destroy()
            co.update()
        # Message to print if equipment is already checked out
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

            # Success message
            message = "Hello " + employee_id1 + " you checked out equipment serial number " + s_num
            messagebox.showinfo("Information!", message, parent=co)
            # Clear text boxes for next entry
            employee_id.delete(0, END)
            s_number.delete(0, END)

    # Submit and Exit buttons
    exit_btn = Button(co, text='Close', command=exit_btn)
    exit_btn.grid(row=4, column=0, columnspan=2, ipadx=110, padx=5, pady=5)
    submit_btn = Button(co, text='Submit', command=submit_btn)
    submit_btn.grid(row=3, column=0, columnspan=2, ipadx=100, padx=5, pady=5)


# Create window and associated entry boxes, labels and buttons for equipment check in into database
def ci_level():
    ci = Toplevel()
    ci.title("Check In Equipment")
    geom = str(SUB_WINDOW_WIDTH) + "x" + str(SUB_WINDOW_HEIGHT)  # Make the string for sub window
    ci.geometry(geom)

    # Create Entry box for Serial Number
    s_number = Entry(ci, width=20)
    s_number.focus()
    s_number.grid(row=1, column=1, padx=5, pady=5)
    # Create drop down box for equipment status (Good or Bad)
    e_status = StringVar()
    e_status.set("Good")
    drop = OptionMenu(ci, e_status,  "Good", "Bad")
    drop.config(width=15)
    drop.grid(row=2, column=1, padx=5, pady=5)

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
        # Get current date and time for check in datetime stamp
        now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        # print(now) #debugging

        # Get entered values for success message box
        e_status1 = e_status.get()
        s_num = s_number.get()
        conn = sqlite3.connect("equipment.db")
        cursor = conn.cursor()
        # Check if equipment already in database and exit with info if not
        cursor.execute("SELECT id FROM equipments WHERE serial_number = ?", (s_num,))
        data = cursor.fetchone()
        cursor.execute("SELECT count(serial_number) FROM check_out_log WHERE serial_number = ? AND time_in is null",
                       (s_num,))
        data2 = cursor.fetchone()[0]
        # print(data2) #debugging
        # Print message if equipment trying to check in is not in database
        if data is None:
            message = "Equipment serial number " + s_num + """ is not in database. 
            Add equipment first & check out if needed"""
            messagebox.showinfo("Information!", message, parent=ci)
            ci.destroy()
            ci.update()
        # Print message if equipment trying to check in is not checked out
        elif data2 == 0:
            message = "Equipment serial number " + s_num + " is not checked out. Please check it out first"
            messagebox.showinfo("Information!", message, parent=ci)
            ci.destroy()
            ci.update()
        else:
            # Enter values into database
            cursor.execute("UPDATE  check_out_log SET time_in = ?, status = ? where serial_number = ?",
                           (now, e_status1, s_num))
            # commit changes
            conn.commit()
            conn.close()

            # Success message
            message = "Hello, you checked in equipment serial number " + s_num
            messagebox.showinfo("Information!", message, parent=ci)
            # Clear text boxes
            # e_status.delete(0, END) # Needed if using text box
            s_number.delete(0, END)

    # Submit and Exit buttons
    exit_btn = Button(ci, text='Close', command=exit_btn)
    exit_btn.grid(row=4, column=0, columnspan=2, ipadx=110, padx=5, pady=5)
    submit_btn = Button(ci, text='Submit', command=submit_btn)
    submit_btn.grid(row=3, column=0, columnspan=2, ipadx=100, padx=5, pady=5)

# Create window for reporting the list of equipment already in the database


def query_eqp():
    qe = Toplevel()
    qe.title("Equipment List")
    geom = str(SUB_WINDOW_WIDTH) + "x" + str(SUB_WINDOW_HEIGHT)  # Make the string for sub window
    qe.geometry(geom)
    #connect to database
    conn = sqlite3.connect("equipment.db")
    cursor = conn.cursor()
    # Select all equipment
    cursor.execute("SELECT * FROM equipments")
    records = cursor.fetchall()
    # Check to be sure there are equipment in the db. May not really be needed
    if records is None:
        message = "There are no equipment in the database, please use Add Equipment to add"
        messagebox.showinfo("Information!", message, parent=qe)
        qe.destroy()
        qe.update()
    # print(records)
    #set up variables to use in storing records
    print_id = ""
    print_type = ""
    print_serial = ""
    # create a list of records for each column in table
    for record in records:
        print_id += str(record[0]) + "\n"
    for record in records:
        print_type += str(record[1]) + "\n"
    for record in records:
        print_serial += str(record[2]) + "\n"

    # debugging
    # print(print_id)
    # print(print_type)
    # print(print_serial)

    # create labels for the column headings
    text_label = Label(qe, text="List of equipment in database")
    text_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
    id_label = Label(qe, text="Number", width=7)
    id_label.grid(row=1, column=0, padx=5, pady=5)
    type_label = Label(qe, text="Equipment Type", width=12)
    type_label.grid(row=1, column=1, padx=5, pady=5)
    serial_label = Label(qe, text="Serial Number", width=12)
    serial_label.grid(row=1, column=2, padx=5, pady=5)

    #create labels for the column data
    id_label_data = Label(qe, text=print_id, width=7)
    id_label_data.grid(row=2, column=0, padx=5, pady=5)
    type_label_data = Label(qe, text=print_type, width=12)
    type_label_data.grid(row=2, column=1, padx=5, pady=5)
    serial_label_data = Label(qe, text=print_serial, width=12)
    serial_label_data.grid(row=2, column=2, padx=5, pady=5)

    # commit changes
    conn.commit()
    conn.close()

    # Exit button function
    def exit_btn():
        qe.destroy()
        qe.update()

    # Submit and Exit buttons
    exit_btn = Button(qe, text='Close', command=exit_btn, width=15)
    exit_btn.grid(row=3, column=1, padx=5, pady=5)

# create a list of records for each column in table


def query_log():
    ql = Toplevel()
    ql.title("Equipment Log")
    # geom = str(SUB_WINDOW_WIDTH) + "x" + str(SUB_WINDOW_HEIGHT)  # Make the string for sub window
    # custom size for log window
    ql.geometry("650x600")

    conn = sqlite3.connect("equipment.db")
    cursor = conn.cursor()
    # Check if equipment already in database and exit with info if not
    cursor.execute("SELECT * FROM check_out_log")
    records = cursor.fetchall()
    # Check to be sure there are records in the db. May not really be needed
    if records is None:
        message = "There are no equipment in the log, please check out / check in equipment"
        messagebox.showinfo("Information!", message, parent=ql)
        ql.destroy()
        ql.update()
    # print(records)

    # set up variables to use in storing records
    print_id = ""
    print_emp_id = ""
    print_serial = ""
    print_chk_out_date = ""
    print_chk_in_date = ""
    print_status = ""

    # create a list of records for each column in table
    for record in records:
        print_id += str(record[0]) + "\n"
    for record in records:
        print_emp_id += str(record[1]) + "\n"
    for record in records:
        print_serial += str(record[2]) + "\n"
    for record in records:
        print_chk_out_date += str(record[3]) + "\n"
    for record in records:
        my_record1 = record[4]
        if my_record1 is None:
            my_record1 = "-"
        print_chk_in_date += str(my_record1) + "\n"
    for record in records:
        my_record2 = record[5]
        if my_record2 is None:
            my_record2 = "-"
        print_status += str(my_record2) + "\n"

    # debugging
    # print(print_id)
    # print(print_emp_id)
    # print(print_serial)
    # print(print_chk_out_date)
    # print(print_chk_in_date)
    # print(print_status)

    # create labels for the column headings
    text_label = Label(ql, text="Equipment Check Out / In Log (Last 20 items)")
    text_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
    id_label = Label(ql, text="Number", width=7)
    id_label.grid(row=1, column=0, padx=5, pady=5)
    emp_id_label = Label(ql, text="Employee ID", width=12)
    emp_id_label.grid(row=1, column=1, padx=5, pady=5)
    serial_label = Label(ql, text="Serial Number", width=12)
    serial_label.grid(row=1, column=2, padx=5, pady=5)
    chk_out_date_label = Label(ql, text="Check Out Date", width=16)
    chk_out_date_label.grid(row=1, column=3, padx=5, pady=5)
    chk_in_date_label = Label(ql, text="Check In Date", width=16)
    chk_in_date_label.grid(row=1, column=4, padx=5, pady=5)
    status_label = Label(ql, text="Status", width=8)
    status_label.grid(row=1, column=5, padx=5, pady=5)

    # create labels for the column data
    id_label_data = Label(ql, text=print_id, width=7)
    id_label_data.grid(row=2, column=0, padx=5, pady=5)
    emp_id_label_data = Label(ql, text=print_emp_id, width=12)
    emp_id_label_data.grid(row=2, column=1, padx=5, pady=5)
    serial_label_data = Label(ql, text=print_serial, width=12)
    serial_label_data.grid(row=2, column=2, padx=5, pady=5)
    chk_out_date_label_data = Label(ql, text=print_chk_out_date, width=16)
    chk_out_date_label_data.grid(row=2, column=3, padx=5, pady=5)
    chk_in_date_label_data = Label(ql, text=print_chk_in_date, width=16)
    chk_in_date_label_data.grid(row=2, column=4, padx=5, pady=5)
    status_label_data = Label(ql, text=print_status, width=8)
    status_label_data.grid(row=2, column=5, padx=5, pady=5)

    # commit changes
    conn.commit()
    conn.close()

    # Exit button function
    def exit_btn():
        ql.destroy()
        ql.update()

    # Submit and Exit buttons
    exit_btn = Button(ql, text='Close', command=exit_btn, width=15)
    exit_btn.grid(row=3, column=3, padx=5, pady=5)


# create the equipments table if not exists already
def create_table_equipment():
    conn = sqlite3.connect("equipment.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS equipments(
    id INTEGER PRIMARY KEY,
    type text,
    serial_number text
    )""")

    #commit changes
    conn.commit()
    conn.close()


# create the log table if not exists already
def create_table_log():
    conn = sqlite3.connect("equipment.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS check_out_log(
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
