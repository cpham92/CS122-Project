import tkinter as tk
from tkinter import messagebox

class NewProfileWindow:
    """
    Window for creating new user profiles
    """
    def __init__(self, root, user_manager):
        self.root = root
        self.user_manager = user_manager

        self.top = tk.Toplevel(root)
        self.top.title("Create New Profile")
        self.top.geometry("350x200")

        tk.Label(self.top, text="New Profile", font=("Arial", 14)).pack(pady=10)

        # --- Username and password entry fields ---
        frame = tk.Frame(self.top)
        frame.pack(pady=10)

        tk.Label(frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)

        self.username_entry = tk.Entry(frame)
        self.username_entry.grid(row=0, column=1)

        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1)

        # --- Buttons ---
        btn_frame = tk.Frame(self.top)
        btn_frame.pack(pady=10)

        create_btn = tk.Button(btn_frame, text="Register", width=10, command=self.create_profile)
        create_btn.grid(row=0, column=0, padx=10)

        cancel_btn = tk.Button(btn_frame, text="Cancel", width=10, command=self.cancel)
        cancel_btn.grid(row=0, column=1, padx=10)

    # --- Helper methods ---
    def create_profile(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            self.user_manager.create_user(username, password)
            messagebox.showinfo("Success", "Profile created successfully!")
            self.top.destroy()
            login_window = self.root.login_window_instance
            login_window.refresh_user_list()
            login_window.reset_fields()
            self.root.deiconify()
        except Exception:
            messagebox.showerror("Error", "Username already exists.")

    def cancel(self):
        self.top.destroy()
        # Refresh login window's dropdown & clear fields
        login_window = self.root.login_window_instance
        login_window.refresh_user_list()
        login_window.reset_fields()
        self.root.deiconify()

