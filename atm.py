from ctypes.wintypes import PLARGE_INTEGER
from email import message
from struct import pack
from tabnanny import check
import tkinter as tk
from tkinter import messagebox, simpledialog

#Data 
balance = 1000000
correct_pin = "0567"
attempt = 0

#global app window
app = tk.Tk()
app.title("Faseeh international Bank")
app.geometry("500x500")

def main_menu():
    clear_screen()
    tk.Label(app, text="ATM Main Menu", font=("Arial", 16)).pack(pady=10)

def login_screen():
    clear_screen()
    tk.Label(app, text="Enter your pin", font=("Arial",15)).pack(pady=20)
    pin_entry = tk.Entry(app, show="*", font=("Arial",15))
    pin_entry.pack()


    def verify_pin():
        global attempts, correct_pin
        pin = pin_entry.get()
        if pin == correct_pin:
            messagebox.showinfo("Sucess", "PIN verified")
            main_menu()
        else:
            attempt += 1
            if attempts < 3:
                messagebox.showwarning("Wrong PIN" f"Wrong PIN! attempts left {3-attempts}")
            else:
                messagebox.showerror("Blocked", "Too many wrong attempts. Card blocked")
                app.destroy()
    


    tk.Button(app, text="Enter", command=verify_pin, font=("Arial",12)).pack(pady=10)
    tk.Button(app, text="1. Check Balance", command=check_balance, width=30, height=2).pack(pady=5)
    tk.Button(app, text="2. Deposit", command=deposit, width=30, height=2).pack(pady=5)
    tk.Button(app, text="3. Withdraw", command=withdraw, width=30, height=2).pack(pady=5)
    tk.Button(app, text="4. Change PIN", command=change_pin, width=30, height=2).pack(pady=5)
    tk.Button(app, text="5. Exit", command=app.destroy, width=30, height=2).pack(pady=5)

def check_balance():
    messagebox.showinfo("Balance", f"Your current balance is ${balance}")

def deposit():
    global balance
    try:
        amount = simpledialog.askinteger("Deposit", "Enter amount to deposit: ")
        if amount and amount > 0:
            balance += amount
            messagebox.showinfo("Success", f"${amount} deposited successfully")
        else:
            messagebox.showwarning("INvalid", "Invalid deposit amount")
    except:
        pass

def withdraw():
    global balance
    try:
        amount = simpledialog.askinteger("Withdraw", "Enter amount to Withdraw: ")
        if amount and amount > 0:
            balance += amount
            messagebox.showinfo("Success", f"${amount} withdrawn successfully")
        else:
            messagebox.showwarning("INvalid", "Invalid withdrawn amount")
    except:
        pass


def change_pin():
    global correct_pin
    current = simpledialog.askstring("Change PIN", "Enter current PIN:", show="*")
    if current == correct_pin:
        new_pin = simpledialog.askstring("Change PIN", "Enter new PIN:", show="*")
        confirm = simpledialog.askstring("Change PIN", "Confirm new PIN:", show="*")
        if new_pin == confirm:
            correct_pin = new_pin
            messagebox.showinfo("Success", "PIN changed successfully!")
        else:
            messagebox.showwarning("Mismatch", "New PINs do not match.")
    else:
        messagebox.showerror("Error", "Incorrect current PIN.")

def clear_screen():
    for widget in app.winfo_children():
        widget.destroy()

login_screen()
app.mainloop()






