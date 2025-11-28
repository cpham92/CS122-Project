import tkinter as tk
from tkinter import ttk, messagebox
from views.new_profile import NewProfileWindow
from views.dashboard import DashboardWindow

class LoginWindow:
    """
    Window that shows upon app startup; users can log in to existing profile or create new profile
    """
    def __init__(self, root, user_manager, task_manager, goal_manager, history_manager):
        self.root = root
        self.user_manager = user_manager
        self.task_manager = task_manager
        self.goal_manager = goal_manager
        self.history_manager = history_manager

        self.root.login_window_instance = self

        self.root.title("Login")
        self.root.geometry("400x230")

        tk.Label(root, text="Welcome to TaskFriend!", font=("Arial", 14)).pack(pady=20)

        # --- Username and password entry fields ---
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Select Profile:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)

        usernames = self.user_manager.get_all_usernames()
        self.username_var = tk.StringVar()

        self.dropdown = ttk.Combobox(
            frame,
            textvariable=self.username_var,
            values=usernames,
            state="readonly",
            width=25
        )
        self.dropdown.grid(row=0, column=1)

        self.password_entry = tk.Entry(frame, show="*", width=26)
        self.password_entry.grid(row=1, column=1)

        # --- Buttons ---
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=25)

        login_btn = tk.Button(btn_frame, text="Login", width=12, command=self.login)
        login_btn.grid(row=0, column=0, padx=10)

        new_profile_btn = tk.Button(btn_frame, text="New Profile", width=12, command=self.open_new_profile_window)
        new_profile_btn.grid(row=0, column=1, padx=10)

    # --- Helper methods ---
    def login(self):
        username = self.username_var.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be blank.")
            return

        # Check if username and hashed password match
        user = self.user_manager.verify_user_credentials(username, password)

        if user is None:
            messagebox.showerror("Login Failed", "Incorrect password.")
            return

        messagebox.showinfo("Success", f"Welcome back, {username}!")
        self.open_dashboard_window(user)

    def refresh_user_list(self):
        # Refresh username list after creating new profile
        usernames = self.user_manager.get_all_usernames()
        self.dropdown["values"] = usernames

    def reset_fields(self):
        # Clear password field when returning to login window
        self.password_entry.delete(0, tk.END)
        self.username_var.set("")

    def open_dashboard_window(self, user):
        self.root.withdraw()
        DashboardWindow(self.root, user, self.user_manager, self.task_manager, self.goal_manager, self.history_manager)

    def open_new_profile_window(self):
        self.root.withdraw()
        NewProfileWindow(self.root, self.user_manager)