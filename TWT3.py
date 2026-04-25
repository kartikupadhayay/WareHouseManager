from tkinter import *
from tkinter import ttk
import snowflake.connector
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from tkcalendar import DateEntry

conn = snowflake.connector.connect(
    user="DBMSProject",
    password="Kartik@123456789",
    account="QVEGFEQ-NK31118",  # e.g. xyz12345.us-east-1
    warehouse="COMPUTE_WH",
    database="DBMS_Project",
    schema="Warehouse"
)


class close_button():
    def __init__(self, prev, curr, ip):
        base_dir = os.path.dirname(__file__)  # folder of current script
        file_path = os.path.join(base_dir, ip)
        self.image = Image.open(file_path)
        self.image = self.image.resize((20, 20))
        self.img = ImageTk.PhotoImage(self.image)
        self.prev = prev
        self.curr = curr
        self.button = Button(self.curr, image=self.img)

    def set_command(self, com):
        self.button.config(command=com)

    def rev(self):
        self.curr.destroy()
        self.prev.deiconify()

    def pack(self):
        self.button.pack(side=RIGHT, anchor='ne')


class edit_values(Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        #self.root.withdraw()
        self.geometry('600x300')
        self.title('Second')
        self.cls = close_button(self.root, self, "close button icon.png")
        self.cls.set_command(self.cls.rev)
        self.cls.pack()

    def insert_widgets(self):
        self.title("Insertion")
        frame = Frame(self)
        frame = Frame(self)
        frame.grid_columnconfigure(0, weight=1, pad=10)
        frame.grid_columnconfigure(1, weight=2, pad=10)
        frame.pack()
        id_label = Label(frame, text='Item_Id: ', font=('Serif', 15, "bold"), width=20)
        id_label.grid(row=0, column=0, pady=10)
        name_label = Label(frame, text='Name: ', font=('Serif', 15, "bold"), width=20)
        name_label.grid(row=1, column=0, pady=10)
        price_label = Label(frame, text='Price: ', font=('Serif', 15, "bold"), width=20)
        price_label.grid(row=3, column=0, pady=10)
        Quantity_label = Label(frame, text='Quantity: ', font=('Serif', 15, "bold"), width=20)
        Quantity_label.grid(row=2, column=0, pady=10)
        self.id_entry = Entry(frame, font=('Serif', 15), width=20, bd=2, relief="solid")
        self.id_entry.grid(row=0, column=1)
        self.name_entry = Entry(frame, font=('Serif', 15), width=20, bd=2, relief="solid")
        self.name_entry.grid(row=1, column=1)
        self.price_entry = Entry(frame, font=('Serif', 15), width=20, bd=2, relief="solid")
        self.price_entry.grid(row=3, column=1)
        self.Quantity_entry = Entry(frame, font=('Serif', 15), width=20, bd=2, relief="solid")
        self.Quantity_entry.grid(row=2, column=1)
        self.button = Button(frame, font=('Serif', 15), padx=5, pady=2)
        self.button.grid(row=4, column=0, columnspan=2, pady=20)

    def config_button(self, com, name):
        self.button.config(command=com, text=name)

    def add_search_widget(self):
        self.attributes('-fullscreen', True)
        att = ['Quantity', 'price']
        com = ['=', '>', '>=', '<', '<=']
        frame = Frame(self)
        frame = Frame(self)
        frame.grid_columnconfigure(0, weight=1, pad=10)
        frame.grid_columnconfigure(1, weight=2, pad=10)
        frame.pack()
        self.att_choice = ttk.Combobox(frame, values=att,)
        self.att_choice.grid(row=1, column=0, pady=10, padx=10)
        self.com_choice = ttk.Combobox(frame, values=com)
        self.com_choice.grid(row=1, column=1, pady=5)
        value_label = Label(frame, text='Value: ', font=('Serif', 15, "bold"), pady=5)
        value_label.grid(row=0, column=0, pady=20)
        self.value_entry = Entry(frame, font=('Serif', 15), relief="solid")
        self.value_entry.grid(row=0, column=1, pady=5)
        self.button = Button(frame, font=('Serif', 15), padx=5, pady=2)
        self.button.grid(row=5, column=0, columnspan=2, pady=90)

    def sort_select(self):
        self.title("Search")
        x = self.value_entry.get()
        att = self.att_choice.get()
        opp = self.com_choice.get()
        self.att_choice.config(state=DISABLED)
        self.com_choice.config(state=DISABLED)
        self.value_entry.config(state=DISABLED)
        self.button.config(state=DISABLED)
        cursor = conn.cursor()
        query = f"SELECT * FROM stock WHERE {att} {opp} %s;"
        cursor.execute(query, (x,))
        rows = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        tree = ttk.Treeview(self,columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for row in rows:
            tree.insert("", END, values=row)
        tree.pack(fill='both', expand=True)
        cursor.close()

    def insert(self):
        id = self.id_entry.get()
        name = self.name_entry.get()
        price = self.price_entry.get()
        amount = self.Quantity_entry.get()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO stock VALUES(%s,%s,%s,%s)", (id, name, amount, price))
            conn.commit()
            messagebox.showinfo("Insertion", "Insertion Successful")
        except EXCEPTION as e:
            messagebox.showerror("Insertion", "Insertion Error !")

    def delete_widgets(self):
        self.title("Deletion")
        frame = Frame(self)
        frame.grid_columnconfigure(0, weight=1, pad=10)
        frame.grid_columnconfigure(1, weight=2, pad=10)
        frame.pack()
        id_label = Label(frame, text='Item_Id: ', font=('Serif', 15, "bold"), width=20, pady=5)
        id_label.grid(row=1,column=0, pady=20)
        self.id_entry = Entry(frame, font=('Serif', 15, "bold"), width=20, bd=2, relief="solid")
        self.id_entry.grid(row=1, column=1)
        self.button = Button(frame, font=('Serif', 15), padx=5, pady=2)
        self.button.grid(row=2, column=0, columnspan=2)


    def delete(self):
        id = self.id_entry.get()
        cursor = conn.cursor()
        q = messagebox.askyesno("Deletion", "Are you sure you want to delete ?")
        if q:
            try:
                cursor.execute("DELETE FROM stock WHERE item_id = %s", (id,))
                conn.commit()
                messagebox.showinfo("Deletion", "Deletion Successful")
            except Exception as e:
                messagebox.showerror("Deletion", "Deletion Error")

    def update_widgets(self):
        self.title("Updation")
        frame = Frame(self)
        frame.grid_columnconfigure(0, weight=1, pad=10)
        frame.grid_columnconfigure(1, weight=2, pad=10)
        frame.pack()
        id_label = Label(frame, text='Item_Id: ', font=('Serif', 15, "bold"), width=20, pady=5)
        id_label.grid(row=1, column=0, pady=40)
        self.id_entry = Entry(frame, font=('Serif', 15), width=20, bd=2, relief="solid")
        self.id_entry.grid(row=1, column=1, pady=20)
        price_label = Label(frame, text='Price: ', font=('Serif', 15, "bold"), width=20, pady=5)
        price_label.grid(row=3, column=0,pady=10)
        self.price_entry = Entry(frame, font=('Serif', 15), width=20, bd=2, relief="solid")
        self.price_entry.grid(row=3, column=1)
        amount_label = Label(frame, text='Quantity: ', font=('Serif', 15, "bold"), width=20, pady=5)
        amount_label.grid(row=2, column=0,pady=10)
        self.Quantity_entry = Entry(frame, font=('Serif', 15), width=20, bd=2, relief="solid")
        self.Quantity_entry.grid(row=2, column=1)
        self.button = Button(frame, font=('Serif', 15), padx=5)
        self.button.grid(row=4, column=0, columnspan=2, pady=20)

    def update(self):
        id = self.id_entry.get()
        price = self.price_entry.get()
        amount = self.Quantity_entry.get()
        try:
            cursor = conn.cursor()
            if(self.id_entry.get().strip() == ""):
                messagebox.showerror("Updation", "Please provide Item_Id")
                return
            elif(self.price_entry.get().strip() != "" and self.Quantity_entry.get().strip() != ""):
                cursor.execute("UPDATE stock SET price = %s, Quantity = %s WHERE item_id = %s", (price, amount, id))
            elif(self.Quantity_entry.get().strip() != ""):
                cursor.execute("UPDATE stock SET Quantity = %s WHERE item_id = %s", (amount, id))
            elif(self.price_entry.get().strip() != ""):
                cursor.execute("UPDATE stock SET price = %s WHERE item_id = %s", (price, id))
            else:
                messagebox.showerror("Updation","Please provide amount or price")
                return
            conn.commit()
            messagebox.showinfo("Updation", "Updation Successful")
            cursor.close()
        except Exception as e:
            messagebox.showerror("Updation", "Upadation Error")

    def delivery(self):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM delivery")
        rows = cursor.fetchall()
        columns = ("Delivery_Id", "Item_Id", "Date of Shipping", "Quantity", "Price")
        tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for i, row in enumerate(rows):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", END, values=row, tags=(tag,))
        tree.tag_configure("oddrow", background="#ecf0f1")
        tree.tag_configure("evenrow", background="#bdc3c7")
        tree.pack(expand=True, fill="both")

    def add_stock_widget(self):
        self.title("Stock Addition")
        frame = Frame(self)
        frame.grid_columnconfigure(0, weight=1, pad=10)
        frame.grid_columnconfigure(1, weight=2, pad=10)
        frame.pack()
        id_label = Label(frame, text='Item_Id: ', font=('Serif', 15, "bold"), width=20, pady=5)
        id_label.grid(row=1, column=0, pady=20)
        self.id_entry = Entry(frame, font=('Serif', 15), width=20, bd=2, relief="solid")
        self.id_entry.grid(row=1, column=1, pady=20)
        amount_label = Label(frame, text='Quantity: ', font=('Serif', 15, "bold"), width=20, pady=5)
        amount_label.grid(row=2, column=0)
        self.Quantity_entry = Entry(frame, font=('Serif', 15, "bold"), width=20, bd=2, relief="solid")
        self.Quantity_entry.grid(row=2, column=1)
        self.button = Button(frame, font=('Serif', 15), padx=5)
        self.button.grid(row=4, column=0, columnspan=2, pady=20)

    def add_stock(self):
        id = self.id_entry.get()
        quantity = self.Quantity_entry.get()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE stock SET Quantity = Quantity + %s WHERE item_id = %s", (quantity, id))
            conn.commit()
            messagebox.showinfo("Stock Addition", "Insertion Successful")
        except EXCEPTION as e:
            messagebox.showerror("Stock Addition", "Insertion Error !")


    def add_delivery_widget(self):
        self.title("Add To Delivery")
        frame = Frame(self)
        frame.grid_columnconfigure(0, weight=1, pad=10)
        frame.grid_columnconfigure(1, weight=2, pad=10)
        frame.pack()
        deliveryid_label = Label(frame, text='Delivery_Id: ', font=('Serif', 15, "bold"), width=20, pady=5)
        deliveryid_label.grid(row=0, column=0, pady=10)
        id_label = Label(frame, text='Item_Id: ', font=('Serif', 15, "bold"), pady=5)
        id_label.grid(row=1, column=0, pady=10)
        date_label = Label(frame, text='Shipping Date: ', font=('Serif', 15, "bold"), width=20, pady=5)
        date_label.grid(row=2, column=0, pady=10)
        Quantity_label = Label(frame, text='Quantity: ', font=('Serif', 15, "bold"), width=20, pady=5)
        Quantity_label.grid(row=3, column=0, pady=10)
        self.deliveryid_entry = Entry(frame, font=('Serif', 15), width=20, bd=2, relief="solid")
        self.deliveryid_entry.grid(row=-0, column=1)
        self.id_entry = Entry(frame, font=('Serif', 15), width=20, bd=2, relief="solid")
        self.id_entry.grid(row=1, column=1)
        self.date_entry = DateEntry(frame,font=('Serif', 15),width=20, bd=2,relief="solid",date_pattern="yyyy-mm-dd")
        self.date_entry.grid(row=2, column=1)
        self.Quantity_entry = Entry(frame, font=('Serif', 15), width=20, bd=2, relief="solid")
        self.Quantity_entry.grid(row=3, column=1)
        self.button = Button(frame, font=('Serif', 15), padx=5, pady=2)
        self.button.grid(row=6, column=0, columnspan=2, pady=20)

    def add_delivery(self):
        did = self.deliveryid_entry.get()
        id = self.id_entry.get()
        date = self.date_entry.get()
        quantity = int(self.Quantity_entry.get())
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM stock WHERE item_id = %s", (id,))
        row = cursor.fetchone()
        if row:
            mrp = int(row[0])
            price = mrp * quantity
        else:
            messagebox.showerror("Delivery Insertion", "Item not found!")
            self.destroy()
        cursor.close()
        cursor = conn.cursor()
        cursor.execute("SELECT quantity FROM stock WHERE item_id = %s", (id,))
        row = cursor.fetchone()
        if row:
            stock_quantity = int(row[0])
        else:
            messagebox.showerror("Delivery Insertion", "Item not found!")
            self.destroy()
        cursor.close()
        cursor = conn.cursor()
        if(stock_quantity >= quantity):
            try:
                cursor.execute("INSERT INTO delivery values(%s,%s,%s,%s,%s)", (did, id, date, quantity, price))
                cursor.close()
                cursor = conn.cursor()
                cursor.execute("UPDATE stock SET quantity = quantity - %s WHERE item_id = %s", (quantity, id))
                messagebox.showinfo("Delivery Insertion", "Insertion successful")
                conn.commit()
                cursor.close()
            except Exception as e:
                messagebox.showerror("Delivery Insertion", "Insertion error")
        else:
            messagebox.showerror("Delivery Insertion", "Not enough product in stock")



def base_destroy(root):
    root.destroy()


def get_data():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stock")
    rows = cursor.fetchall()
    cursor.close()
    return rows


def refresh(tree):
    for item in tree.get_children():
        tree.delete(item)

    rows = get_data()
    for i, row in enumerate(rows):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert("", END, values=row, tags=(tag,))
    tree.tag_configure("oddrow", background="#ecf0f1")
    tree.tag_configure("evenrow", background="#bdc3c7")