import tkinter as tk
from tkinter import ttk

from db.database import Database
from controllers.user_manager import UserManager
from controllers.task_manager import TaskManager
from controllers.goal_manager import GoalManager
from controllers.history_manager import HistoryManager

from views.login import LoginWindow

def main():
    # Create the actual main window for the entire app
    root = tk.Tk()
    root.title("TaskFriend")
    root.geometry("400x200")
    style = ttk.Style(root)
    style.theme_use("classic")

    # ---- Initialize managers ----
    db = Database()
    user_manager = UserManager(db)
    task_manager = TaskManager(db)
    goal_manager = GoalManager(db)
    history_manager = HistoryManager(db)

    # ---- Launch Login Window (root is the login window) ----
    LoginWindow(root, user_manager, task_manager, goal_manager, history_manager)

    # ---- Start the Tk event loop ----
    root.mainloop()


if __name__ == "__main__":
    main()
