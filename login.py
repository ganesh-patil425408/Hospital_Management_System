import tkinter as tk
from tkinter import ttk, messagebox
from excel_manager import validate_login, register_user, username_exists


class LoginPage:
    def __init__(self, root, open_dashboard):
        self.root = root
        self.open_dashboard = open_dashboard
        self.root.title("Hospital Management System - Login")
        self.root.geometry("500x560")
        self.root.resizable(False, False)
        self.root.configure(bg="Light Blue")
        self.login_ui()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def login_ui(self):
        self.clear()
        card = tk.Frame(self.root, bg="White", bd=1, relief="solid")
        card.place(relx=.5, rely=.5, anchor="center", width=420, height=450)

        tk.Label(card, text="🏥", font=("Arial", 38), bg="White").pack(pady=(18, 0))
        tk.Label(card, text="Hospital Management System", font=("Arial", 18, "bold"),
                 fg="Dark Blue", bg="White").pack(pady=5)
        tk.Label(card, text="Login to continue", fg="Grey", bg="White").pack(pady=(0, 20))

        form = tk.Frame(card, bg="White")
        form.pack(fill="x", padx=45)

        tk.Label(form, text="Username", bg="White", anchor="w").pack(fill="x")
        self.username = ttk.Entry(form)
        self.username.pack(fill="x", ipady=5, pady=(4, 12))

        tk.Label(form, text="Password", bg="White", anchor="w").pack(fill="x")
        self.password = ttk.Entry(form, show="*")
        self.password.pack(fill="x", ipady=5, pady=(4, 18))

        ttk.Button(form, text="LOGIN", command=self.login).pack(fill="x", ipady=5)
        tk.Button(card, text="New user? Register here", command=self.register,
                  bg="White", fg="Blue", bd=0, font=("Arial", 10, "bold")).pack(pady=18)

        self.username.focus()
        self.root.bind("<Return>", lambda e: self.login())

    def login(self):
        username = self.username.get().strip()
        password = self.password.get()

        if not username or not password:
            messagebox.showwarning("Required", "Enter username and password.")
            return

        if validate_login(username, password):
            self.root.unbind("<Return>")
            self.open_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self):
        self.clear()
        card = tk.Frame(self.root, bg="White", bd=1, relief="solid")
        card.place(relx=.5, rely=.5, anchor="center", width=440, height=520)

        tk.Label(card, text="Create Account", font=("Arial", 21, "bold"),
                 fg="Dark Blue", bg="White").pack(pady=(22, 5))
        tk.Label(card, text="Register as Hospital Staff", fg="Grey", bg="White").pack(pady=(0, 15))

        form = tk.Frame(card, bg="White")
        form.pack(fill="x", padx=45)
        self.reg = {}

        for name, secret in [
            ("Full Name", False), ("Username", False), ("Email", False),
            ("Password", True), ("Confirm Password", True)
        ]:
            tk.Label(form, text=name, bg="White", anchor="w").pack(fill="x")
            e = ttk.Entry(form, show="*" if secret else "")
            e.pack(fill="x", ipady=5, pady=(3, 8))
            self.reg[name] = e

        ttk.Button(form, text="REGISTER", command=self.save_register).pack(fill="x", ipady=5, pady=5)
        tk.Button(form, text="← Back to Login", command=self.login_ui,
                  bg="White", fg="Blue", bd=0).pack(pady=8)

    def save_register(self):
        full = self.reg["Full Name"].get().strip()
        username = self.reg["Username"].get().strip()
        email = self.reg["Email"].get().strip()
        password = self.reg["Password"].get()
        confirm = self.reg["Confirm Password"].get()

        if not all([full, username, email, password, confirm]):
            messagebox.showwarning("Required", "Fill all fields.")
        elif "@" not in email:
            messagebox.showwarning("Email", "Enter a valid email address.")
        elif len(password) < 4:
            messagebox.showwarning("Password", "Password must have at least 4 characters.")
        elif password != confirm:
            messagebox.showerror("Password", "Passwords do not match.")
        elif username_exists(username):
            messagebox.showerror("Username", "Username already exists.")
        elif register_user(username, password, full, email):
            messagebox.showinfo("Success", "Account created. Please login.")
            self.login_ui()
        else:
            messagebox.showerror("Error", "Registration failed.")
