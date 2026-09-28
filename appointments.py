import tkinter as tk
from tkinter import ttk, messagebox
from excel_manager import get_records, add_record, update_record, delete_record, APPOINTMENT_HEADERS


class AppointmentPage:
    def __init__(self, root, back):
        self.root, self.back = root, back
        for w in root.winfo_children(): w.destroy()
        root.title("Hospital Management System - Appointments")
        root.geometry("1100x680")
        self.create_ui(); self.load_records()

    def create_ui(self):
        header = tk.Frame(self.root, bg="Dark Blue"); header.pack(fill="x")
        tk.Button(header, text="← Dashboard", command=self.back, bg="Dark Blue", fg="White", bd=0,
                  font=("Arial", 10, "bold")).pack(side="left", padx=20, pady=18)
        tk.Label(header, text="Appointment Management", bg="Dark Blue", fg="White",
                 font=("Arial", 20, "bold")).pack(side="left")

        body = tk.Frame(self.root, bg="Light Blue"); body.pack(fill="both", expand=True, padx=18, pady=18)
        form = tk.LabelFrame(body, text="Appointment Details", bg="White", font=("Arial", 11, "bold")); form.pack(fill="x", pady=(0, 10))
        self.entries = []

        for i, name in enumerate(APPOINTMENT_HEADERS):
            r, c = (i // 4) * 2, i % 4
            tk.Label(form, text=name, bg="White").grid(row=r, column=c, sticky="w", padx=8, pady=(7, 2))
            if name == "Status":
                e = ttk.Combobox(form, values=["Scheduled", "Completed", "Cancelled"], state="readonly", width=21)
            else:
                e = ttk.Entry(form, width=23)
            e.grid(row=r + 1, column=c, padx=8, pady=(0, 7), ipady=3); self.entries.append(e)

        buttons = tk.Frame(body, bg="Light Blue"); buttons.pack(fill="x", pady=(0, 8))
        for text, cmd in [("Add", self.add), ("Update", self.update), ("Delete", self.delete), ("Clear", self.clear)]:
            tk.Button(buttons, text=text, command=cmd, width=11).pack(side="left", padx=4)

        search = tk.Frame(body, bg="Light Blue"); search.pack(fill="x", pady=(0, 8))
        tk.Label(search, text="Search ID / Patient:", bg="Light Blue").pack(side="left")
        self.search_entry = ttk.Entry(search, width=30); self.search_entry.pack(side="left", padx=8, ipady=3)
        ttk.Button(search, text="Search", command=self.search).pack(side="left")
        ttk.Button(search, text="Show All", command=self.load_records).pack(side="left", padx=5)

        frame = tk.Frame(body); frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(frame, columns=APPOINTMENT_HEADERS, show="headings")
        for col in APPOINTMENT_HEADERS:
            self.tree.heading(col, text=col); self.tree.column(col, width=130, anchor="center")
        y = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview); x = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y.set, xscrollcommand=x.set)
        self.tree.grid(row=0, column=0, sticky="nsew"); y.grid(row=0, column=1, sticky="ns"); x.grid(row=1, column=0, sticky="ew")
        frame.grid_rowconfigure(0, weight=1); frame.grid_columnconfigure(0, weight=1)
        self.tree.bind("<<TreeviewSelect>>", self.select)

    def values(self): return [e.get().strip() for e in self.entries]

    def add(self):
        v = self.values()
        if not v[0] or not v[1] or not v[3]:
            messagebox.showwarning("Required", "Appointment ID, Patient ID and Doctor are required."); return
        if any(str(r[0]) == v[0] for r in get_records("Appointments")):
            messagebox.showerror("Duplicate", "Appointment ID already exists."); return
        add_record("Appointments", v); messagebox.showinfo("Success", "Appointment added successfully.")
        self.clear(); self.load_records()

    def select(self, event=None):
        s = self.tree.selection()
        if s:
            for e, value in zip(self.entries, self.tree.item(s[0], "values")):
                e.delete(0, tk.END); e.insert(0, value)

    def update(self):
        v = self.values()
        if not v[0]: messagebox.showwarning("Required", "Select an appointment first."); return
        if update_record("Appointments", 1, v[0], v): messagebox.showinfo("Success", "Appointment updated successfully."); self.load_records()
        else: messagebox.showerror("Error", "Appointment not found.")

    def delete(self):
        aid = self.entries[0].get().strip()
        if not aid: messagebox.showwarning("Required", "Select an appointment first."); return
        if messagebox.askyesno("Confirm Delete", "Delete this appointment?"):
            if delete_record("Appointments", 1, aid): messagebox.showinfo("Deleted", "Appointment deleted successfully."); self.clear(); self.load_records()

    def clear(self):
        for e in self.entries: e.set("") if isinstance(e, ttk.Combobox) else e.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())

    def load_records(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in get_records("Appointments"): self.tree.insert("", "end", values=row)

    def search(self):
        q = self.search_entry.get().strip().lower()
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in get_records("Appointments"):
            if not q or q in str(row[0]).lower() or q in str(row[1]).lower() or q in str(row[2]).lower(): self.tree.insert("", "end", values=row)
