from tkinter import *
from tkinter import ttk,messagebox
import snowflake.connector
from PIL import Image,ImageTk
from TWT3 import *

def styled_entry(parent):
    return Entry(parent, font=("Segoe UI", 13), bd=2, relief="solid")



def insertion():
    sec = edit_values(root)
    sec.insert_widgets()
    sec.config_button(sec.insert,'Insertion')

def search():
    sec = edit_values(root)
    sec.add_search_widget()
    sec.config_button(sec.sort_select, "Search")

def delete():
    sec = edit_values(root)
    sec.delete_widgets()
    sec.config_button(sec.delete, "Delete")

def update():
    sec = edit_values(root)
    sec.update_widgets()
    sec.config_button(sec.update, "Confirm")

def delivery():
    sec = edit_values(root)
    sec.delivery()

def add_stock():
    sec = edit_values(root)
    sec.add_stock_widget()
    sec.config_button(sec.add_stock, "Confirm")

def add_delivery():
    sec = edit_values(root)
    sec.add_delivery_widget()
    sec.config_button(sec.add_delivery, "Place")


root = Tk()
# Apply global styles
style = ttk.Style()
style.theme_use("clam")

style.configure("TButton",
                font=("Segoe UI", 13),
                padding=10)

style.configure("Treeview.Heading",
                font=("Segoe UI", 12, "bold"),
                background="#34495e",
                foreground="white")

style.configure("Treeview",
                font=("Segoe UI", 11),
                rowheight=28)

# Apply global styles after root is created
style2 = ttk.Style()
style2.theme_use("clam")

style2.configure("TButton",
                font=("Segoe UI", 13),
                padding=10,
                relief="flat",
                background="#3498db",
                foreground="white")
style2.map("TButton",
          background=[("active", "#2980b9")])


root.configure(bg="#f4f6f7")

toolbar = Frame(root, bg="#34495e")
toolbar.pack(side="top", fill="x")

root.title("WareHouse Manager")
root.geometry("650x800")
#root.attributes('-fullscreen', True)
x = close_button(None, root,"close button icon.png")
x.set_command(lambda : base_destroy(root))
x.pack()
r = close_button(None, root,"undo.png")
r.set_command(lambda : refresh(tree))
r.pack()
mainlabel = Label(root,
                  font=("Impact", 28, "bold"),
                  text="WareHouse Manager",
                  width=20,
                  height=2,
                  fg="#2c3e50",
                  bg="#f4f6f7")
mainlabel.pack(pady=20)
frame = Frame(root, bg="#dfe6e9", bd=2, relief="groove")
frame.grid_columnconfigure(0, weight=1)  # stretch column
frame.grid_columnconfigure(1, weight=1)
frame.pack(side='left', fill="y", padx=15, pady=15)

button1 = Button(frame, font=('Serif', 18), text="Add New Item", command=insertion, width=20)
button1.grid(row=0, column=0, columnspan=2, pady=10)
button2 = Button(frame, font=('Serif', 18), text="Delivery",command=delivery, width=20)
button2.grid(row=5, column=0, columnspan=2, pady=10)
button3 = Button(frame, font=('Serif', 18), text="Remove Item",command=delete, width=20)
button3.grid(row=1, column=0, columnspan=2, pady=10)
button4 = Button(frame, font=('Serif', 18), text="Add stock",command=add_stock, width=20)
button4.grid(row=2, column=0, columnspan=2, pady=10)
button5 = Button(frame, font=('Serif', 18), text="Search", command=search, width=20)
button5.grid(row=4, column=0, columnspan=2, pady=10)
button6 = Button(frame, font=('Serif', 18), text="Add to delivery",command=add_delivery, width=20)
button6.grid(row=6, column=0, columnspan=2, pady=10)
button7 = Button(frame, font=('Serif', 18), text="Update", command=update, width=20)
button7.grid(row=3, column=0, columnspan=2, pady=10)

rows = get_data()
columns = ("Item_Id", "Item_name", "Quantity", "Price")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
for i, row in enumerate(rows):
    tag = "evenrow" if i % 2 == 0 else "oddrow"
    tree.insert("", END, values=row, tags=(tag,))
tree.tag_configure("oddrow", background="#ecf0f1")
tree.tag_configure("evenrow", background="#bdc3c7")
tree.pack(expand=True, fill="both", side='right')

root.mainloop()