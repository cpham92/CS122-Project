import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser

class SettingsWindow:
    def __init__(self, root, user, user_manager, settings_manager,
                 task_manager, goal_manager, history_manager, dashboard):
        self.root = root
        self.user = user
        self.user_manager = user_manager
        self.settings_manager = settings_manager
        self.task_manager = task_manager
        self.goal_manager = goal_manager
        self.history_manager = history_manager
        self.dashboard = dashboard

        self.top = tk.Toplevel(root)
        self.top.title("Settings")
        self.top.geometry("470x475")
        self.top.grab_set()

        # Load settings
        self.colors = self.settings_manager.get_settings(self.user.user_id)

        # --- Profile management ---
        profile_frame = tk.LabelFrame(self.top, text="Profile Settings", padx=10, pady=10)
        profile_frame.pack(fill="x", padx=15, pady=10)

        # Username change
        tk.Label(profile_frame, text="Username:").grid(row=0, column=0, sticky="w")
        self.username_entry = tk.Entry(profile_frame, width=25)
        self.username_entry.grid(row=0, column=1, padx=5)
        self.username_entry.insert(0, self.user.username)

        tk.Button(profile_frame, text="Change", command=self.change_username).grid(row=0, column=2, padx=10)

        # Password change
        tk.Label(profile_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        tk.Button(profile_frame, text="Change Password", command=self.change_password).grid(row=1, column=1, pady=5)

        # Delete profile
        tk.Button(profile_frame, text="Delete Profile", fg="red", command=self.delete_profile).grid(
            row=2, column=0, columnspan=3, pady=10
        )

        # --- Color customization ---
        colors_frame = tk.LabelFrame(self.top, text="Task Color Settings", padx=10, pady=10)
        colors_frame.pack(fill="x", padx=15, pady=10)

        self.color_widgets = {}
        row = 0

        for label, key in [
            ("High Priority", "high"),
            ("Medium Priority", "medium"),
            ("Low Priority", "low"),
            ("Completed Tasks", "completed"),
            ("Overdue Tasks", "overdue")
        ]:
            tk.Label(colors_frame, text=label + ":").grid(row=row, column=0, sticky="w", pady=5)

            preview = tk.Label(colors_frame, width=10, bg=self.colors[key], relief="solid")
            preview.grid(row=row, column=1, padx=5)
            self.color_widgets[key] = preview

            tk.Button(colors_frame, text="Change",
                      command=lambda k=key: self.pick_color(k)).grid(row=row, column=2, padx=5)
            row += 1

        btn_frame = tk.Frame(self.top)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Save Settings", width=15, command=self.save_settings).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Cancel", width=15, command=self.top.destroy).grid(row=0, column=1, padx=10)

    # --- Profile methods ---
    def change_username(self):
        new_name = self.username_entry.get().strip()
        if not new_name:
            messagebox.showerror("Error", "Username cannot be empty.")
            return

        self.user_manager.update_username(self.user.user_id, new_name)
        self.dashboard.update_username_display(new_name)
        self.root.login_window_instance.refresh_user_list()
        self.user.username = new_name
        messagebox.showinfo("Updated", "Username updated successfully.")

    def change_password(self):
        old_pass = simpledialog.askstring("Current Password", "Enter your current password:", show="*")
        if not old_pass or not self.user.verify_password(old_pass):
            messagebox.showerror("Error", "Incorrect password.")
            return

        new_pass = simpledialog.askstring("New Password", "Enter new password:", show="*")
        confirm = simpledialog.askstring("Confirm Password", "Confirm new password:", show="*")

        if not new_pass or new_pass != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        self.user.password = new_pass
        self.user_manager.update_password(self.user.user_id, self.user.password)
        messagebox.showinfo("Updated", "Password updated successfully.")

    def delete_profile(self):
        confirm = messagebox.askyesno(
            "Delete Profile",
            "Are you sure you want to permanently delete your profile?\nThis cannot be undone.",
            icon="warning"
        )
        if not confirm:
            return

        # Delete all user information
        self.user_manager.delete_user(self.user.user_id)
        self.task_manager.delete_all_tasks_for_user(self.user.user_id)
        self.goal_manager.delete_all_goals_for_user(self.user.user_id)
        self.history_manager.delete_all_history_for_user(self.user.user_id)

        messagebox.showinfo("Deleted", "Your profile has been deleted.")
        self.root.login_window_instance.refresh_user_list()
        self.root.login_window_instance.reset_fields()
        self.top.destroy()
        self.root.deiconify()  # show login
        self.dashboard.top.destroy()  # close dashboard

    # --- Color picker ---
    def pick_color(self, key):
        color = colorchooser.askcolor(title="Choose Color")[1]
        if color:
            self.colors[key] = color
            self.color_widgets[key].config(bg=color)

    def save_settings(self):
        self.settings_manager.save_settings(self.user.user_id, self.colors)

        self.user.color_settings = self.colors.copy()

        messagebox.showinfo("Saved", "Settings saved successfully!")

        # Refresh dashboard colors
        self.dashboard.apply_color_theme(self.colors)
        self.dashboard.refresh_tasks()

        self.top.destroy()
