import tkinter as tk
from tkinter import ttk
from excel_manager import get_records


class Dashboard:
    def __init__(self, root, logout):
        self.root, self.logout = root, logout
        self.root.title("Hospital Management System - Dashboard")
        self.root.geometry("1050x650")
        self.root.minsize(900, 600)
        self.root.configure(bg="Light Blue")
        self.create_ui()

    def create_ui(self):
        for w in self.root.winfo_children(): w.destroy()
        header = tk.Frame(self.root, bg="Dark Blue"); header.pack(fill="x")
        tk.Label(header, text="🏥 Hospital Management System", font=("Arial", 21, "bold"), fg="White", bg="Dark Blue").pack(side="left", padx=25, pady=18)
        tk.Button(header, text="Logout", command=self.logout, bg="Red", fg="White", bd=0, width=10).pack(side="right", padx=25)

        body = tk.Frame(self.root, bg="Light Blue"); body.pack(fill="both", expand=True, padx=30, pady=30)
        tk.Label(body, text="Dashboard", font=("Arial", 25, "bold"), fg="Dark Blue", bg="Light Blue").pack(anchor="w")
        tk.Label(body, text="Manage patients and appointments easily", fg="Grey", bg="Light Blue").pack(anchor="w", pady=(5, 25))

        cards = tk.Frame(body, bg="Light Blue"); cards.pack(fill="x")
        self.card(cards, "Total Patients", len(get_records("Patients")), 0)
        self.card(cards, "Appointments", len(get_records("Appointments")), 1)

        tk.Label(body, text="Navigation", font=("Arial", 18, "bold"), fg="Dark Blue", bg="Light Blue").pack(anchor="w", pady=(40, 15))
        nav = tk.Frame(body, bg="Light Blue"); nav.pack(fill="x")
        tk.Button(nav, text="👤 Patient Management", command=self.open_patients, width=25, height=3).pack(side="left", padx=(0, 15))
        tk.Button(nav, text="📅 Appointment Management", command=self.open_appointments, width=25, height=3).pack(side="left")

    def card(self, parent, title, value, col):
        f = tk.Frame(parent, bg="White", bd=1, relief="solid", width=250, height=110); f.grid(row=0, column=col, padx=(0, 20)); f.pack_propagate(False)
        tk.Label(f, text=title, bg="White", fg="Grey", font=("Arial", 11)).pack(anchor="w", padx=20, pady=(18, 0))
        tk.Label(f, text=str(value), bg="White", fg="Dark Blue", font=("Arial", 28, "bold")).pack(anchor="w", padx=20)

    def open_patients(self):
        from patients import PatientPage
        PatientPage(self.root, self.create_ui)

    def open_appointments(self):
        from appointments import AppointmentPage
        AppointmentPage(self.root, self.create_ui)
