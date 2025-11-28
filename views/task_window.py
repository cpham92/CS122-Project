import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
from datetime import datetime

class TaskWindow:
    """
    Window used for creating new tasks and updating existing tasks
    """
    def __init__(self, root, user, task_manager, goal_manager, history_manager, task=None):
        self.root = root
        self.user = user
        self.task_manager = task_manager
        self.goal_manager = goal_manager
        self.history_manager = history_manager
        self.task = task  # None = new task mode; otherwise edit task mode

        self.top = tk.Toplevel(root)
        self.top.title("Task")
        self.top.geometry("525x350")

        form = tk.Frame(self.top)
        form.pack(pady=10)

        # Name
        tk.Label(form, text="Task Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(form, width=40)
        self.name_entry.grid(row=0, column=1, pady=5)

        # Description
        tk.Label(form, text="Description:").grid(row=1, column=0, sticky="nw", pady=5)
        self.desc_entry = tk.Entry(form, width=40)
        self.desc_entry.grid(row=1, column=1, pady=5)

        # Deadline
        tk.Label(form, text="Deadline:").grid(row=2, column=0, sticky="w", pady=5)

        self.deadline_entry = tk.Entry(form, width=17, fg="gray")
        self.deadline_entry.grid(row=2, column=1, sticky="w", pady=5)

        # If editing an existing task, populate the deadline
        if self.task and self.task.deadline:
            self.deadline_entry.delete(0, tk.END)
            self.deadline_entry.insert(0, self.task.deadline.strftime("%Y-%m-%d"))
            self.deadline_entry.config(fg="black")
        elif self.task:
            self.deadline_entry.config(fg="gray")  # placeholder already inserted

        # Placeholder text
        self.deadline_entry.insert(0, "YYYY-MM-DD")

        # Handle placeholder behavior
        self.deadline_entry.bind("<FocusIn>", self._clear_deadline_placeholder)
        self.deadline_entry.bind("<FocusOut>", self._add_deadline_placeholder)

        # Priority
        tk.Label(form, text="Priority:").grid(row=3, column=0, sticky="w", pady=5)
        self.priority_var = tk.StringVar()
        self.priority_dropdown = ttk.Combobox(
            form,
            textvariable=self.priority_var,
            values=["High", "Medium", "Low"],
            state="readonly",
            width=17
        )
        self.priority_dropdown.grid(row=3, column=1, sticky="w", pady=5)

        # Category
        tk.Label(form, text="Category:").grid(row=4, column=0, sticky="w", pady=5)
        self.category_var = tk.StringVar()
        categories = self._get_category_list()
        self.category_dropdown = ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            width=17
        )
        self.category_dropdown.grid(row=4, column=1, sticky="w", pady=5)
        self.category_dropdown.bind("<<ComboboxSelected>>", self.handle_category_selection)

        # Goal
        tk.Label(form, text="Goal:").grid(row=5, column=0, sticky="w", pady=5)
        self.goal_var = tk.StringVar()
        goals = self._get_goal_list()
        self.goal_dropdown = ttk.Combobox(
            form,
            textvariable=self.goal_var,
            values=goals,
            state="readonly",
            width=17
        )
        self.goal_dropdown.grid(row=5, column=1, sticky="w", pady=5)

        # Completed
        tk.Label(form, text="Mark Completed:").grid(row=6, column=0, sticky="w", pady=5)
        self.completed_var = tk.IntVar()
        self.completed_checkbox = tk.Checkbutton(
            form, variable=self.completed_var
        )
        self.completed_checkbox.grid(row=6, column=1, sticky="w", pady=5)

        # --- Buttons ---
        btn_frame = tk.Frame(self.top)
        btn_frame.pack(pady=20)

        save_btn = tk.Button(btn_frame, text="Save Task", width=15, command=self.save_task)
        save_btn.grid(row=0, column=0, padx=10)

        delete_btn = tk.Button(btn_frame, text="Delete Task", width=15, command=self.delete_task)
        delete_btn.grid(row=0, column=1, padx=10)

        # If editing, load task fields
        if self.task:
            self.load_task()

    # --- Helper methods ---
    def _get_category_list(self):
        tasks = self.task_manager.get_tasks_for_user(self.user.user_id)
        categories = sorted({t.category for t in tasks if t.category})
        categories.append("<New Category>")
        categories.append("<Manage Categories>")
        categories.append("")  # blank option
        return categories

    def _get_goal_list(self):
        goals = self.goal_manager.get_goals_for_user(self.user.user_id)
        names = [g.name for g in goals]
        names.append("")  # blank option
        return names

    def _clear_deadline_placeholder(self, event):
        if self.deadline_entry.get() == "YYYY-MM-DD":
            self.deadline_entry.delete(0, tk.END)
            self.deadline_entry.config(fg="black")

    def _add_deadline_placeholder(self, event):
        if not self.deadline_entry.get():
            self.deadline_entry.insert(0, "YYYY-MM-DD")
            self.deadline_entry.config(fg="gray")

    def refresh_category_list(self):
        categories = self._get_category_list()
        self.category_dropdown["values"] = categories

    def handle_category_selection(self, event):
        selected = self.category_var.get()

        if selected == "<New Category>":
            self.create_new_category()
            return

        if selected == "<Manage Categories>":
            self.manage_categories()
            return

    def create_new_category(self):
        new_category = simpledialog.askstring("New Category", "Enter category name:")
        if new_category:
            self.category_var.set(new_category)
        else:
            self.category_var.set("")

        self.refresh_category_list()

    def manage_categories(self):
        categories = [c for c in self._get_category_list()
                      if c not in ("", "<New Category>", "<Manage Categories>")]

        if not categories:
            messagebox.showinfo("No Categories", "You have no categories to manage.")
            return

        category = simpledialog.askstring(
            "Manage Categories",
            "Enter the category name to modify:\n" +
            "(Available: " + ", ".join(categories) + ")"
        )

        if not category or category not in categories:
            return

        action = self.ask_category_action(category)

        if action == "rename":
            self.rename_category(category)
        elif action == "delete":
            self.delete_category(category)
        else:
            return

    def ask_category_action(self, category):
        """
        Custom dialog to confirm user action for category management.
        """
        dialog = tk.Toplevel(self.top)
        dialog.title("Category Options")
        dialog.geometry("425x100")
        dialog.grab_set()  # Make dialog modal

        tk.Label(dialog, text=f"What would you like to do with '{category}'?").pack(pady=15)

        result = {"choice": None}

        def choose(option):
            result["choice"] = option
            dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Rename", width=10, command=lambda: choose("rename")).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Delete", width=10, command=lambda: choose("delete")).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Cancel", width=10, command=lambda: choose("cancel")).grid(row=0, column=2, padx=5)

        dialog.wait_window()
        return result["choice"]

    def rename_category(self, old_name):
        new_name = simpledialog.askstring(
            "Rename Category",
            f"Enter a new name for '{old_name}':"
        )

        if not new_name or new_name.strip() == "":
            return

        new_name = new_name.strip()

        self.task_manager.update_category(self.user.user_id, old_name, new_name)

        # If editing a task and the category was this one, update it
        if self.category_var.get() == old_name:
            self.category_var.set(new_name)

        messagebox.showinfo("Success", f"Category renamed to '{new_name}'.")
        self.refresh_category_list()

    def delete_category(self, category):
        if not messagebox.askyesno(
                "Confirm Delete",
                f"Delete category '{category}'?\nTasks will not be deleted."
        ):
            return

        self.task_manager.remove_category(self.user.user_id, category)

        if self.category_var.get() == category:
            self.category_var.set("")

        messagebox.showinfo("Success", f"Category '{category}' deleted.")
        self.refresh_category_list()

    def load_task(self):
        self.name_entry.insert(0, self.task.name)

        if self.task.description:
            self.desc_entry.insert(0, self.task.description)

        if self.task.deadline:
            # Fill the date in YYYY-MM-DD format
            self.deadline_entry.delete(0, tk.END)
            self.deadline_entry.insert(0, self.task.deadline.strftime("%Y-%m-%d"))
            self.deadline_entry.config(fg="black")
        else:
            # Show placeholder
            self.deadline_entry.delete(0, tk.END)
            self.deadline_entry.insert(0, "YYYY-MM-DD")
            self.deadline_entry.config(fg="gray")

        self.priority_var.set(self.task.priority)

        self.category_var.set(self.task.category or "")

        self.completed_var.set(self.task.completed)

        goal = ""
        if self.task.goal_id:
            goal_obj = self.goal_manager.get_goal_by_id(self.task.goal_id)
            if goal_obj:
                goal = goal_obj.name
        self.goal_var.set(goal)

    def save_task(self):
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        deadline_str = self.deadline_entry.get().strip()
        # If blank or still placeholder, treat as None
        if deadline_str == "" or deadline_str == "YYYY-MM-DD":
            deadline = None
        else:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid date format",
                                     "Please enter the deadline in YYYY-MM-DD format.")
                return
        priority = self.priority_var.get()
        category = self.category_var.get().strip()
        goal_name = self.goal_var.get()
        completed = self.completed_var.get()

        if not name:
            messagebox.showerror("Error", "Task name is required.")
            return
        if not priority:
            messagebox.showerror("Error", "Priority is required.")
            return

        goal_id = None
        if goal_name:
            goals = self.goal_manager.get_goals_for_user(self.user.user_id)
            for g in goals:
                if g.name == goal_name:
                    goal_id = g.goal_id
                    break

        # Updating existing task
        if self.task:
            self.task.name = name
            self.task.description = description if description else None
            self.task.deadline = deadline
            self.task.priority = priority
            self.task.category = category if category else None
            self.task.goal_id = goal_id

            if completed:
                timestamp = datetime.now()
                self.task.mark_complete(timestamp)
                self.task_manager.mark_task_complete(self.task.task_id, timestamp.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                self.task.mark_incomplete()
                self.task_manager.mark_task_incomplete(self.task.task_id)

            self.task_manager.update_task(self.task)
            messagebox.showinfo("Success", "Task updated.")
            self.top.destroy()
            return

        # Creating new task
        date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.task_manager.create_task(
            self.user.user_id,
            goal_id,
            name,
            description if description else None,
            deadline if deadline else None,
            priority,
            category if category else None,
            date_created
        )

        messagebox.showinfo("Success", "Task created.")
        self.top.destroy()

    def delete_task(self):
        # Close window if creating new task
        if not self.task:
            self.top.destroy()
            return

        # Delete task if editing
        if messagebox.askyesno("Confirm Delete", "Delete this task?"):
            self.task_manager.delete_task(self.task.task_id)
            messagebox.showinfo("Deleted", "Task deleted.")
            self.top.destroy()
