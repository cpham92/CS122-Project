import tkinter as tk
from tkinter import ttk, messagebox

class GoalWindow:
    """
    Window used for creating new goals and updating existing goals
    """
    def __init__(self, root, user, goal_manager, task_manager, goal=None):
        self.root = root
        self.user = user
        self.goal_manager = goal_manager
        self.task_manager = task_manager
        self.goal = goal  # None = new goal mode; otherwise edit goal mode

        self.top = tk.Toplevel(root)
        self.top.title("Goal")
        self.top.geometry("600x500")

        # --- Goal name and description entry fields ---
        header = tk.Frame(self.top)
        header.pack(fill="x", pady=10, padx=15)

        tk.Label(header, text="Goal Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(header, width=45)
        self.name_entry.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(header, text="Description:").grid(row=1, column=0, sticky="w", pady=5)
        self.description_entry = tk.Entry(header, width=45)
        self.description_entry.grid(row=1, column=1, sticky="w", pady=5)

        # --- Progress bar ---
        self.progress_label_var = tk.StringVar(value="Progress: 0% Completed")
        tk.Label(header, textvariable=self.progress_label_var).grid(
            row=2, column=0, sticky="w", pady=10
        )

        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress_bar = ttk.Progressbar(
            header, orient="horizontal", length=300, mode="determinate",
            variable=self.progress_var, maximum=100
        )
        self.progress_bar.grid(row=2, column=1, sticky="w", pady=10)

        ttk.Separator(self.top, orient="horizontal").pack(fill="x", padx=10, pady=5)

        # --- Table containing tasks belonging to selected goal ---
        body = tk.Frame(self.top)
        body.pack(fill="both", expand=True, padx=15, pady=10)

        tk.Label(body, text="Tasks:").pack(anchor="w")

        columns = ("completed", "name", "deadline", "priority")
        self.tree = ttk.Treeview(
            body, columns=columns, show="headings", selectmode="browse", height=10
        )

        self.tree.heading("completed", text="Completed")
        self.tree.heading("name", text="Task")
        self.tree.heading("deadline", text="Deadline")
        self.tree.heading("priority", text="Priority")

        self.tree.column("completed", width=90, anchor="center")
        self.tree.column("name", width=220, anchor="w")
        self.tree.column("deadline", width=120, anchor="center")
        self.tree.column("priority", width=90, anchor="center")

        self.apply_color_theme(self.user.color_settings)

        # Detect selection to enable Remove Task button
        self.tree.bind("<<TreeviewSelect>>", self.handle_task_select)

        self.tree.pack(fill="both", expand=True, pady=5)

        # --- Buttons ---
        btn_frame = tk.Frame(self.top)
        btn_frame.pack(pady=10)

        save_btn = tk.Button(btn_frame, text="Save Goal", width=15, command=self.save_goal)
        save_btn.grid(row=0, column=0, padx=10)

        self.remove_task_btn = tk.Button(btn_frame, text="Remove Task", width=15,
                                    command=self.remove_selected_task_from_goal, state="disabled")
        self.remove_task_btn.grid(row=0, column=1, padx=10)

        delete_btn = tk.Button(btn_frame, text="Delete Goal", width=15, command=self.delete_goal)
        delete_btn.grid(row=0, column=2, padx=10)

        # --- Init mode ---
        if self.goal:
            # Edit/view mode
            self.name_entry.insert(0, self.goal.name)
            if self.goal.description:
                self.description_entry.insert(0, self.goal.description)
            self.load_tasks_for_goal()
        else:
            # Create mode
            self.update_progress(0, 0)
            self.remove_task_btn.config(state="disabled")

    # --- Helper methods ---
    def load_tasks_for_goal(self):
        """
        Load tasks for selected goal, sort and color, and update progress.
        """
        # Clear previous rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not self.goal:
            self.update_progress(0, 0)
            return

        all_tasks = self.task_manager.get_tasks_for_user(self.user.user_id)
        goal_tasks = [t for t in all_tasks if t.goal_id == self.goal.goal_id]

        # Sort: incomplete first by priority, then completed at bottom
        priority_order = {"High": 0, "Medium": 1, "Low": 2}

        def sort_key(task):
            is_completed = 1 if getattr(task, "completed", 0) else 0
            prio_rank = priority_order.get(task.priority, 999)
            return (is_completed, prio_rank)

        goal_tasks.sort(key=sort_key)

        completed_count = 0

        for task in goal_tasks:
            completed = getattr(task, "completed", 0)
            if completed:
                completed_text = "✓"
                tag = "completed"
                completed_count += 1
            else:
                completed_text = ""
                if task.is_overdue():
                    tag = "overdue"
                elif task.priority == "High":
                    tag = "high"
                elif task.priority == "Medium":
                    tag = "medium"
                else:
                    tag = "low"

            deadline_str = task.deadline.strftime("%Y-%m-%d") if task.deadline else ""
            values = (completed_text, task.name, deadline_str, task.priority)
            # Store task_id in iid so we can find it on selection
            self.tree.insert("", "end", iid=str(task.task_id), values=values, tags=(tag,))

        self.update_progress(completed_count, len(goal_tasks))

    def apply_color_theme(self, colors):
        self.tree.tag_configure("high", background=colors["high"])
        self.tree.tag_configure("medium", background=colors["medium"])
        self.tree.tag_configure("low", background=colors["low"])
        self.tree.tag_configure("completed", background=colors["completed"])
        self.tree.tag_configure("overdue", background=colors["overdue"])

    def handle_task_select(self, event):
        """
        Enable 'remove task' button if task is selected.
        :param event: Task selected
        :return:
        """
        selected = self.tree.selection()
        if selected:
            self.remove_task_btn.config(state="normal")
        else:
            self.remove_task_btn.config(state="disabled")

    def update_progress(self, completed_count, total_count):
        """
        Update progress bar and label.
        :param completed_count: Number of completed tasks in goal
        :param total_count: Total number of tasks in goal
        """
        if total_count == 0:
            percent = 0
        else:
            percent = int((completed_count / total_count) * 100)

        self.progress_var.set(percent)
        self.progress_label_var.set(f"Progress: {percent}% Completed")


    def save_goal(self):
        name = self.name_entry.get().strip()
        description = self.description_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Goal name is required.")
            return

        if self.goal is None:
            # Create mode
            goal_id = self.goal_manager.create_goal(
                self.user.user_id,
                name,
                description if description else None
            )
            messagebox.showinfo("Success", "Goal created.")
            self.top.destroy()
        else:
            # Edit mode
            self.goal.name = name
            self.goal.description = description if description else None
            self.goal_manager.update_goal(self.goal)
            messagebox.showinfo("Success", "Goal updated.")
            self.top.destroy()

    def remove_selected_task_from_goal(self):
        """
        Remove the selected task from the goal without deleting the task itself.
        """
        if self.goal is None:
            messagebox.showinfo("Info", "No tasks to remove for a new goal.")
            return

        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to remove.")
            return

        task_id = int(selected[0])  # task_id was stored as iid
        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            messagebox.showerror("Error", "Task not found.")
            return

        if not messagebox.askyesno("Confirm", "Remove selected task from this goal?"):
            return

        # Detach task from goal but keep it in DB
        task.goal_id = None
        self.task_manager.update_task(task)

        # Refresh the table and progress
        self.load_tasks_for_goal()

    def delete_goal(self):
        """
        Delete the selected goal along with all of its associated tasks.
        """
        if self.goal is None:
            self.top.destroy()
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete this goal along with all of its tasks?"
        )
        if not confirm:
            return

        # Delete all tasks belonging to this goal
        all_tasks = self.task_manager.get_tasks_for_user(self.user.user_id)
        for task in all_tasks:
            if task.goal_id == self.goal.goal_id:
                self.task_manager.delete_task(task.task_id)

        # Delete the goal itself
        self.goal_manager.delete_goal(self.goal.goal_id)

        messagebox.showinfo("Success", "Goal and its tasks deleted.")
        self.top.destroy()

