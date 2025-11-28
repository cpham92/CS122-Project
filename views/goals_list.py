import tkinter as tk
from tkinter import ttk, messagebox

from views.goal_window import GoalWindow


class GoalsListWindow:
    """
    Window where users can view and manage all of their goals
    """
    def __init__(self, root, user, goal_manager, task_manager):
        self.root = root
        self.user = user
        self.goal_manager = goal_manager
        self.task_manager = task_manager

        self.top = tk.Toplevel(root)
        self.top.title("Goals")
        self.top.geometry("650x500")

        # --- Goals table ---
        table_frame = tk.Frame(self.top)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("name", "description", "progress", "task_count")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("name", text="Goal")
        self.tree.heading("description", text="Description")
        self.tree.heading("progress", text="Progress")
        self.tree.heading("task_count", text="Tasks")

        self.tree.column("name", width=200, anchor="w")
        self.tree.column("description", width=220, anchor="w")
        self.tree.column("progress", width=80, anchor="center")
        self.tree.column("task_count", width=80, anchor="center")

        # Detect selection to enable Edit Goal button
        self.tree.bind("<<TreeviewSelect>>", self.handle_selection)

        # --- Buttons ---
        btn_frame = tk.Frame(self.top)
        btn_frame.pack(pady=10)

        new_goal_btn = tk.Button(btn_frame, text="New Goal", width=14,
                                 command=self.open_new_goal)
        new_goal_btn.grid(row=0, column=0, padx=10)

        self.edit_goal_btn = tk.Button(btn_frame, text="Edit Goal", width=14,
                                       state="disabled", command=self.open_edit_goal)
        self.edit_goal_btn.grid(row=0, column=1, padx=10)

        return_btn = tk.Button(btn_frame, text="Return to Dashboard", width=18,
                               command=self.return_to_dashboard)
        return_btn.grid(row=0, column=2, padx=10)

        # Initialize and populate goal table
        self.refresh_goals()

    # --- Helper methods ---
    def refresh_goals(self):
        """
        Load and refresh all goals for the user into the table.
        """
        # Clear previous rows
        self.tree.delete(*self.tree.get_children())

        goals = self.goal_manager.get_goals_for_user(self.user.user_id)
        tasks = self.task_manager.get_tasks_for_user(self.user.user_id)

        for goal in goals:
            goal_tasks = [t for t in tasks if t.goal_id == goal.goal_id]
            total = len(goal_tasks)
            completed = sum(1 for t in goal_tasks if t.completed == 1)

            # Calculate progress percentage
            if total == 0:
                percent = "0%"
            else:
                percent = f"{int((completed / total) * 100)}%"

            self.tree.insert(
                "",
                "end",
                iid=str(goal.goal_id),   # store goal_id as iid
                values=(
                    goal.name,
                    goal.description or "",
                    percent,
                    total
                )
            )

        self.edit_goal_btn.config(state="disabled")

    def handle_selection(self, event):
        """
        Enable 'edit goal' button if goal is selected.
        :param event: Goal selected
        """
        selected = self.tree.selection()
        if selected:
            self.edit_goal_btn.config(state="normal")
        else:
            self.edit_goal_btn.config(state="disabled")

    def open_new_goal(self):
        window = GoalWindow(self.root, self.user, self.goal_manager, self.task_manager, goal=None)
        self.top.wait_window(window.top)
        self.refresh_goals()

    def open_edit_goal(self):
        # Check if goal is selected
        selected = self.tree.selection()
        if not selected:
            return

        goal_id = int(selected[0])
        goal = self.goal_manager.get_goal_by_id(goal_id)

        if not goal:
            messagebox.showerror("Error", "Goal not found.")
            return

        window = GoalWindow(self.root, self.user, self.goal_manager, self.task_manager, goal=goal)
        self.top.wait_window(window.top)
        self.refresh_goals()

    def return_to_dashboard(self):
        self.top.destroy()
