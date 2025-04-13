import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector as a

# MySQL connection
con = a.connect(
    host="localhost",
    user="root",
    password="sagar",
    database="bank_sys"
)

# ================= Functions ==================

def open_account():
    def submit():
        try:
            acc = int(e1.get())
            name = e2.get()
            dob = e3.get()
            address = e4.get()
            mob = int(e5.get())
            balance = int(e6.get())

            sql1 = "INSERT INTO account VALUES (%s, %s, %s, %s, %s, %s)"
            sql2 = "INSERT INTO amount VALUES (%s, %s, %s)"
            data1 = (acc, name, dob, address, mob, balance)
            data2 = (acc, name, balance)

            c = con.cursor()
            c.execute(sql1, data1)
            c.execute(sql2, data2)
            con.commit()

            messagebox.showinfo("Success", "Account opened successfully!")
            top.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    top = tk.Toplevel()
    top.title("Open New Account")

    labels = ["Account No", "Name", "DOB", "Address", "Mobile No", "Opening Balance"]
    entries = []

    for i, text in enumerate(labels):
        tk.Label(top, text=text).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(top)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    e1, e2, e3, e4, e5, e6 = entries
    tk.Button(top, text="Submit", command=submit).grid(row=6, column=0, columnspan=2, pady=10)

def deposit():
    def submit():
        try:
            acc = int(e1.get())
            amount = int(e2.get())

            c = con.cursor()
            c.execute("SELECT TotalBalance FROM amount WHERE Acc_no=%s", (acc,))
            result = c.fetchone()

            if result:
                new_balance = result[0] + amount
                c.execute("UPDATE amount SET TotalBalance=%s WHERE Acc_no=%s", (new_balance, acc))
                con.commit()
                messagebox.showinfo("Success", "Amount Deposited Successfully!")
                top.destroy()
            else:
                messagebox.showerror("Error", "Account not found!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    top = tk.Toplevel()
    top.title("Deposit Amount")

    tk.Label(top, text="Account No").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(top, text="Amount").grid(row=1, column=0, padx=10, pady=5)
    e1 = tk.Entry(top)
    e2 = tk.Entry(top)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    tk.Button(top, text="Deposit", command=submit).grid(row=2, column=0, columnspan=2, pady=10)

def withdraw():
    def submit():
        try:
            acc = int(e1.get())
            amount = int(e2.get())

            c = con.cursor()
            c.execute("SELECT TotalBalance FROM amount WHERE Acc_no=%s", (acc,))
            result = c.fetchone()

            if result and result[0] >= amount:
                new_balance = result[0] - amount
                c.execute("UPDATE amount SET TotalBalance=%s WHERE Acc_no=%s", (new_balance, acc))
                con.commit()
                messagebox.showinfo("Success", "Amount Withdrawn Successfully!")
                top.destroy()
            else:
                messagebox.showerror("Error", "Insufficient Balance or Account not found!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    top = tk.Toplevel()
    top.title("Withdraw Amount")

    tk.Label(top, text="Account No").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(top, text="Amount").grid(row=1, column=0, padx=10, pady=5)
    e1 = tk.Entry(top)
    e2 = tk.Entry(top)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    tk.Button(top, text="Withdraw", command=submit).grid(row=2, column=0, columnspan=2, pady=10)

def balance():
    def submit():
        try:
            acc = int(e1.get())
            c = con.cursor()
            c.execute("SELECT TotalBalance FROM amount WHERE Acc_no=%s", (acc,))
            result = c.fetchone()
            if result:
                messagebox.showinfo("Balance", f"Current Balance: ₹{result[0]}")
                top.destroy()
            else:
                messagebox.showerror("Error", "Account not found!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    top = tk.Toplevel()
    top.title("Balance Enquiry")

    tk.Label(top, text="Account No").grid(row=0, column=0, padx=10, pady=5)
    e1 = tk.Entry(top)
    e1.grid(row=0, column=1)

    tk.Button(top, text="Check Balance", command=submit).grid(row=1, column=0, columnspan=2, pady=10)

def account_details():
    def submit():
        try:
            acc = int(e1.get())
            c = con.cursor()
            c.execute("SELECT * FROM account WHERE Acc_no=%s", (acc,))
            result = c.fetchone()

            if result:
                details = f"Account No: {result[0]}\nName: {result[1]}\nDOB: {result[2]}\nAddress: {result[3]}\nMobile: {result[4]}\nBalance: ₹{result[5]}"
                messagebox.showinfo("Account Details", details)
                top.destroy()
            else:
                messagebox.showerror("Error", "Account not found!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    top = tk.Toplevel()
    top.title("Account Details")

    tk.Label(top, text="Account No").grid(row=0, column=0, padx=10, pady=5)
    e1 = tk.Entry(top)
    e1.grid(row=0, column=1)

    tk.Button(top, text="Show Details", command=submit).grid(row=1, column=0, columnspan=2, pady=10)

def close_account():
    def submit():
        try:
            acc = int(e1.get())
            c = con.cursor()
            c.execute("DELETE FROM amount WHERE Acc_no=%s", (acc,))
            c.execute("DELETE FROM account WHERE Acc_no=%s", (acc,))
            con.commit()
            messagebox.showinfo("Closed", "Account Deleted Successfully!")
            top.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    top = tk.Toplevel()
    top.title("Close Account")

    tk.Label(top, text="Account No").grid(row=0, column=0, padx=10, pady=5)
    e1 = tk.Entry(top)
    e1.grid(row=0, column=1)

    tk.Button(top, text="Close Account", command=submit).grid(row=1, column=0, columnspan=2, pady=10)

# ================= GUI Main Menu ==================

root = tk.Tk()
root.title("Bank Management System")
root.geometry("600x600")

# Load and place background image
bg_image = Image.open("ChatGPT Image Apr 13, 2025, 03_36_41 PM.png")
bg_image = bg_image.resize((600, 600), Image.Resampling.LANCZOS)

bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=600, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Place widgets on canvas
canvas.create_text(300, 50, font=("Arial", 24, "bold"), fill="white")

button_specs = [
    ("Open New Account", open_account),
    ("Deposit Amount", deposit),
    ("Withdraw Amount", withdraw),
    ("Balance Enquiry", balance),
    ("Account Details", account_details),
    ("Close Account", close_account),
    ("Exit", root.destroy)
]

for i, (text, command) in enumerate(button_specs):
    btn = tk.Button(root, text=text, width=25, command=command)
    canvas.create_window(300, 120 + i * 50, window=btn)

root.mainloop()
