
import tkinter as tk
from excel_manager import create_excel
from login import LoginPage
from dashboard import Dashboard


class HospitalManagementSystem:
    def __init__(self):
        create_excel()

        self.root = tk.Tk()

        self.show_login()

        self.root.mainloop()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()
        LoginPage(
            self.root,
            self.show_dashboard
        )

    def show_dashboard(self):
        self.clear_window()
        Dashboard(
            self.root,
            self.show_login
        )


if __name__ == "__main__":
    HospitalManagementSystem()
