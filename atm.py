
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from datetime import datetime
import hashlib

class ATMApp:
    def __init__(self):
        # All users stored here: username -> user data
        self.users = {
            "faseeh": {
                "pin_hash": self.hash_pin("1234"),
                "balance": 1000,
                "history": [],
                "attempts": 0
            },
            "ali": {
                "pin_hash": self.hash_pin("5678"),
                "balance": 2000,
                "history": [],
                "attempts": 0
            }
        }
        self.current_user = None

        self.window = tk.Tk()
        self.window.title("ATM Simulator")
        self.window.geometry("400x450")

        self.login_screen()
        self.window.mainloop()

    def hash_pin(self, pin):
        return hashlib.sha256(pin.encode()).hexdigest()

    def clear_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.window, text="ATM Login", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self.window, text="Username:", font=("Arial", 14)).pack()
        username_entry = tk.Entry(self.window, font=("Arial", 14))
        username_entry.pack(pady=5)

        tk.Label(self.window, text="PIN:", font=("Arial", 14)).pack()
        pin_entry = tk.Entry(self.window, show="*", font=("Arial", 14))
        pin_entry.pack(pady=5)

        def verify():
            username = username_entry.get()
            pin = pin_entry.get()

            if username not in self.users:
                messagebox.showerror("Login Failed", "User not found.")
                return

            user = self.users[username]

            if user["attempts"] >= 3:
                messagebox.showerror("Blocked", "Too many wrong attempts.")
                return

            if self.hash_pin(pin) == user["pin_hash"]:
                messagebox.showinfo("Success", f"Welcome {username}!")
                self.current_user = username
                self.main_menu()
            else:
                user["attempts"] += 1
                left = 3 - user["attempts"]
                if left > 0:
                    messagebox.showwarning("Wrong PIN", f"Wrong PIN. Attempts left: {left}")
                else:
                    messagebox.showerror("Blocked", "Too many wrong attempts.")
                    self.window.destroy()

        tk.Button(self.window, text="Login", command=verify, font=("Arial", 12), width=15).pack(pady=20)

    def main_menu(self):
        self.clear_screen()
        tk.Label(self.window, text=f"Welcome {self.current_user}", font=("Arial", 16, "bold")).pack(pady=10)

        menu = [
            ("1. Check Balance", self.check_balance),
            ("2. Deposit", self.deposit),
            ("3. Withdraw", self.withdraw),
            ("4. Change PIN", self.change_pin),
            ("5. Transaction History", self.view_history),
            ("6. Logout", self.logout)
        ]

        for text, action in menu:
            tk.Button(self.window, text=text, command=action, width=30, height=2).pack(pady=5)

    def get_user(self):
        return self.users[self.current_user]

    def check_balance(self):
        balance = self.get_user()["balance"]
        messagebox.showinfo("Balance", f"Your current balance is $. {balance}")

    def deposit(self):
        try:
            amount = simpledialog.askinteger("Deposit", "Enter amount to deposit:")
            if amount and amount > 0:
                self.get_user()["balance"] -= amount
                self.add_transaction(f"Deposited $. {amount}")
                messagebox.showinfo("Success", f"$. {amount} deposited successfully.")
            else:
                messagebox.showwarning("Invalid", "Invalid deposit amount.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def withdraw(self):
        try:
            amount = simpledialog.askinteger("Withdraw", "Enter amount to withdraw:")
            if amount and amount > 0:
                user = self.get_user()
                if amount <= user["balance"]:
                    user["balance"] -= amount
                    self.add_transaction(f"Withdrew $. {amount}")
                    messagebox.showinfo("Success", f"$. {amount} withdrawn successfully.")
                else:
                    messagebox.showerror("Failed", "Insufficient balance.")
            else:
                messagebox.showwarning("Invalid", "Invalid withdrawal amount.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def change_pin(self):
        user = self.get_user()
        current = simpledialog.askstring("Change PIN", "Enter current PIN:", show="*")
        if self.hash_pin(current) == user["pin_hash"]:
            new_pin = simpledialog.askstring("Change PIN", "Enter new 4-digit PIN:", show="*")
            confirm = simpledialog.askstring("Change PIN", "Confirm new PIN:", show="*")
            if new_pin == confirm and new_pin.isdigit() and len(new_pin) == 4:
                user["pin_hash"] = self.hash_pin(new_pin)
                self.add_transaction("PIN changed successfully")
                messagebox.showinfo("Success", "PIN changed successfully!")
            else:
                messagebox.showwarning("Mismatch", "PINs do not match or are invalid.")
        else:
            messagebox.showerror("Error", "Incorrect current PIN.")

    def add_transaction(self, detail):
        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.get_user()["history"].append(f"{time_stamp} — {detail}")

    def view_history(self):
        history = self.get_user()["history"]
        if not history:
            messagebox.showinfo("History", "No transactions yet.")
            return

        window = tk.Toplevel(self.window)
        window.title("Transaction History")
        window.geometry("400x300")

        log = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Arial", 12))
        log.pack(expand=True, fill='both')

        for entry in history:
            log.insert(tk.END, entry + "\n")

        log.config(state=tk.DISABLED)

    def logout(self):
        self.current_user = None
        self.login_screen()

# Run the app
ATMApp()
