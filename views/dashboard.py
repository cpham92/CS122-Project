import tkinter as tk
from tkinter import ttk
from datetime import datetime

from views.task_window import TaskWindow
from views.goals_list import GoalsListWindow
from views.settings import SettingsWindow
from views.report_window import ReportWindow  


class DashboardWindow:
    """
    Main window of the app where users can view and manage all of their tasks
    """
    def __init__(self, root, user, user_manager, task_manager, goal_manager, history_manager, settings_manager):
        self.root = root
        self.user = user
        self.user_manager = user_manager
        self.task_manager = task_manager
        self.goal_manager = goal_manager
        self.history_manager = history_manager
        self.settings_manager = settings_manager

        self.top = tk.Toplevel(root)
        self.top.title("Dashboard")
        self.top.geometry("950x600")

        # --- Header (user/settings/logout) ---
        header = tk.Frame(self.top)
        header.pack(fill="x", pady=10, padx=20)

        # Left side (User label)
        left_header = tk.Frame(header)
        left_header.pack(side="left", anchor="w")

        tk.Label(left_header, text="User:", font=("Arial", 14, "bold")).pack(side="left")
        self.username_label = tk.Label(left_header, text=user.username, font=("Arial", 14))
        self.username_label.pack(side="left", padx=5)

        # Right side (Settings + Logout)
        right_header = tk.Frame(header)
        right_header.pack(side="right", anchor="e")

        settings_btn = tk.Button(right_header, text="Settings", width=10, command=self.open_settings)
        settings_btn.pack(side="left", padx=10)

        logout_btn = tk.Button(right_header, text="Logout", width=10, command=self.logout)
        logout_btn.pack(side="left")

        ttk.Separator(self.top, orient="horizontal").pack(fill="x", padx=15, pady=5)

        # --- Filters and sorting ---
        fs_frame = tk.Frame(self.top)
        fs_frame.pack(fill="x", padx=20, pady=10)

        # Configure columns so spacing is even
        for i in range(4):
            fs_frame.grid_columnconfigure(i, weight=1)

        # Filters label
        tk.Label(fs_frame, text="Filters:", font=("Arial", 14, "bold")).grid(
            row=0, column=0, sticky="w"
        )

        # --- Priority Filter ---
        priority_frame = tk.Frame(fs_frame)
        priority_frame.grid(row=0, column=1, padx=10, sticky="w")

        tk.Label(priority_frame, text="Priority").pack(side="left", padx=(0, 5))
        self.filter_priority_var = tk.StringVar()
        self.priority_filter = ttk.Combobox(
            priority_frame, textvariable=self.filter_priority_var,
            values=["", "High", "Medium", "Low"], state="readonly", width=12
        )
        self.priority_filter.pack(side="left")
        self.priority_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_tasks())

        # --- Category Filter ---
        category_frame = tk.Frame(fs_frame)
        category_frame.grid(row=0, column=2, padx=10, sticky="w")

        tk.Label(category_frame, text="Category").pack(side="left", padx=(0, 5))
        self.filter_category_var = tk.StringVar()
        self.category_filter = ttk.Combobox(
            category_frame, textvariable=self.filter_category_var,
            values=self.get_category_list(), state="readonly", width=12
        )
        self.category_filter.pack(side="left")
        self.category_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_tasks())

        # --- Status Filter ---
        status_frame = tk.Frame(fs_frame)
        status_frame.grid(row=0, column=3, padx=10, sticky="w")

        tk.Label(status_frame, text="Status").pack(side="left", padx=(0, 5))
        self.filter_status_var = tk.StringVar()
        self.status_filter = ttk.Combobox(
            status_frame, textvariable=self.filter_status_var,
            values=["", "Completed", "Uncompleted"], state="readonly", width=12
        )
        self.status_filter.pack(side="left")
        self.status_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_tasks())

        tk.Label(fs_frame, text="Sort By:", font=("Arial", 14, "bold")).grid(row=1, column=0, sticky="w", pady=(10, 0))

        self.sort_var = tk.StringVar()

        # Deadline Sort
        deadline_btn = tk.Button(fs_frame, text="Deadline", width=12,
                                 command=lambda: self.set_sort("deadline"))
        deadline_btn.grid(row=1, column=1, pady=10)

        # Priority Sort
        priority_btn = tk.Button(fs_frame, text="Priority", width=12,
                                 command=lambda: self.set_sort("priority"))
        priority_btn.grid(row=1, column=2)

        # Alphabetical Sort
        alpha_btn = tk.Button(fs_frame, text="Alphabetical", width=12,
                              command=lambda: self.set_sort("alphabetical"))
        alpha_btn.grid(row=1, column=3)

        ttk.Separator(self.top, orient="horizontal").pack(fill="x", padx=15, pady=5)

        # --- To-Do List / Task Table ---
        table_frame = tk.Frame(self.top)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(table_frame, text="To-Do List:", font=("Arial", 14, "bold")).pack(anchor="w")

        columns = ("name", "description", "deadline", "priority", "goal")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("name", text="Task")
        self.tree.heading("description", text="Description")
        self.tree.heading("deadline", text="Deadline")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("goal", text="Goal")

        self.tree.column("name", width=150, anchor="w")
        self.tree.column("description", width=150, anchor="w")
        self.tree.column("deadline", width=100, anchor="center")
        self.tree.column("priority", width=100, anchor="center")
        self.tree.column("goal", width=120, anchor="center")

        self.apply_color_theme(self.user.color_settings)

        # Detect selection to enable Edit Task button
        self.tree.bind("<<TreeviewSelect>>", self.handle_task_select)

        # --- Action buttons ---
        button_frame = tk.Frame(self.top)
        button_frame.pack(pady=10)

        new_task_btn = tk.Button(button_frame, text="New Task", width=12,
                                 command=self.open_new_task)
        new_task_btn.grid(row=0, column=0, padx=8)

        self.edit_task_btn = tk.Button(button_frame, text="Edit Task", width=12,
                                       state="disabled", command=self.open_edit_task)
        self.edit_task_btn.grid(row=0, column=1, padx=8)

        view_goals_btn = tk.Button(button_frame, text="View Goals", width=12,
                                   command=self.view_goals)
        view_goals_btn.grid(row=0, column=2, padx=8)

        view_reports_btn = tk.Button(button_frame, text="View Report", width=12,
                                     command=self.view_reports)
        view_reports_btn.grid(row=0, column=3, padx=8)

        # Initialize and populate to-do list
        self.sort_mode = "created"  # default sort by date created
        self.refresh_tasks()

    # --- Helper methods for filters and sorting ---
    def get_category_list(self):
        tasks = self.task_manager.get_tasks_for_user(self.user.user_id)
        categories = sorted({t.category for t in tasks if t.category})
        categories.insert(0, "")  # allow blank/no filter
        return categories

    def refresh_category_list(self):
        categories = self.get_category_list()
        self.category_filter["values"] = categories

    def set_sort(self, mode):
        self.sort_mode = mode
        self.refresh_tasks()

    def apply_filters(self, tasks):
        # Priority
        priority = self.filter_priority_var.get()
        if priority:
            tasks = [t for t in tasks if t.priority == priority]

        # Category
        category = self.filter_category_var.get()
        if category:
            tasks = [t for t in tasks if t.category == category]

        # Status
        status = self.filter_status_var.get()
        if status == "Completed":
            tasks = [t for t in tasks if t.completed == 1]
        elif status == "Uncompleted":
            tasks = [t for t in tasks if t.completed == 0]

        return tasks

    def apply_sorting(self, tasks):
        if self.sort_mode == "deadline":
            return sorted(tasks, key=lambda t: (t.deadline if isinstance(t.deadline, datetime) else datetime.max))
        elif self.sort_mode == "priority":
            rank = {"High": 0, "Medium": 1, "Low": 2}
            return sorted(tasks, key=lambda t: rank.get(t.priority, 99))
        elif self.sort_mode == "alphabetical":
            return sorted(tasks, key=lambda t: t.name.lower())
        else:
            # default: newest first
            return sorted(tasks, key=lambda t: t.date_created, reverse=True)

    def refresh_tasks(self):
        """
        Load tasks for user and refresh table after task creation/update
        """
        # Clear previous rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        tasks = self.task_manager.get_tasks_for_user(self.user.user_id)
        tasks = self.apply_filters(tasks)
        tasks = self.apply_sorting(tasks)

        for t in tasks:
            # Ensure deadline is formatted properly
            if t.deadline:
                deadline = t.deadline.strftime("%Y-%m-%d")
            else:
                deadline = ""

            goal_name = ""
            if t.goal_id:
                g = self.goal_manager.get_goal_by_id(t.goal_id)
                if g:
                    goal_name = g.name

            # Color tag based on priority or completed
            if t.completed:
                tag = "completed"
            elif t.is_overdue():
                tag = "overdue"
            elif t.priority == "High":
                tag = "high"
            elif t.priority == "Medium":
                tag = "medium"
            else:
                tag = "low"

            self.tree.insert(
                "", "end", iid=str(t.task_id),
                values=(t.name, t.description or "", deadline, t.priority, goal_name),
                tags=(tag,)
            )

        # Reset edit button
        self.edit_task_btn.config(state="disabled")

    def handle_task_select(self, event):
        """
        Enable 'edit task' button if task is selected
        :param event: task selected
        """
        selected = self.tree.selection()
        if selected:
            self.edit_task_btn.config(state="normal")
        else:
            self.edit_task_btn.config(state="disabled")

    def apply_color_theme(self, colors):
        self.tree.tag_configure("high", background=colors["high"])
        self.tree.tag_configure("medium", background=colors["medium"])
        self.tree.tag_configure("low", background=colors["low"])
        self.tree.tag_configure("completed", background=colors["completed"])
        self.tree.tag_configure("overdue", background=colors["overdue"])

    def update_username_display(self, new_name):
        self.user.username = new_name
        self.username_label.config(text=new_name)

    # --- Button commands ---
    def open_new_task(self):
        window = TaskWindow(self.root, self.user, self.task_manager, self.goal_manager,
                   self.history_manager, task=None)
        self.top.wait_window(window.top)
        # Refresh tasks and categories
        self.refresh_tasks()
        self.refresh_category_list()

    def open_edit_task(self):
        # Check if task is currently selected
        selected = self.tree.selection()
        if not selected:
            return
        task_id = int(selected[0])
        task = self.task_manager.get_task_by_id(task_id)
        window = TaskWindow(self.root, self.user, self.task_manager, self.goal_manager,
                   self.history_manager, task=task)
        self.top.wait_window(window.top)
        # Refresh lists
        self.refresh_tasks()
        self.refresh_category_list()

    def view_goals(self):
        window = GoalsListWindow(self.root, self.user, self.goal_manager, self.task_manager)
        self.top.wait_window(window.top)
        self.refresh_tasks()

    def view_reports(self):
        ReportWindow(self.top, self.history_manager, self.task_manager, self.user.user_id)

    def open_settings(self):
        SettingsWindow(
            self.root, self.user, self.user_manager,
            self.settings_manager, self.task_manager,
            self.goal_manager, self.history_manager,
            dashboard=self
        )

    def logout(self):
        self.top.destroy()
        # Refresh login window's dropdown & clear password field
        login_window = self.root.login_window_instance
        login_window.refresh_user_list()
        login_window.reset_fields()
        self.root.deiconify()  # show login window again
