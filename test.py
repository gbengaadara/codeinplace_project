import tkinter as tk

def focus_next(event):
    event.widget.tk_focusNext().focus_set()

root = tk.Tk()
e1 = tk.Entry(root)
e1.pack()
e1.focus()
e1.bind("<Return>", focus_next)  # Bind Enter key to focus_next function

e2 = tk.Entry(root)
e2.pack()
e2.bind("<Return>", focus_next)

e3 = tk.Entry(root)
e3.pack()
root.mainloop()

