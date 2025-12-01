import tkinter as tk
from tkinter import ttk

from db.database import Database
from controllers.user_manager import UserManager
from controllers.task_manager import TaskManager
from controllers.goal_manager import GoalManager
from controllers.history_manager import HistoryManager
from controllers.settings_manager import SettingsManager

from views.login import LoginWindow

def main():
    # Main window for the app but it will be hidden so that login is the root window
    root = tk.Tk()
    root.title("TaskFriend")
    root.geometry("400x200")
    style = ttk.Style(root)
    style.theme_use("classic")

    # --- Initialize managers ---
    db = Database()
    user_manager = UserManager(db)
    task_manager = TaskManager(db)
    goal_manager = GoalManager(db)
    history_manager = HistoryManager(db)
    settings_manager = SettingsManager(db)

    # Launch login window as root
    LoginWindow(root, user_manager, task_manager, goal_manager, history_manager, settings_manager)

    # ---- Start the Tk event loop ----
    root.mainloop()


if __name__ == "__main__":
    main()
