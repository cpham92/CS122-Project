from models.task import Task
from controllers.history_manager import HistoryManager

class TaskManager:
    def __init__(self, db):
        self.conn = db.get_connection()
        self.db = db

    def create_task(self, user_id, goal_id, name, description, deadline, priority, category, date_created):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO tasks
                (user_id, goal_id, name, description, deadline,
                 priority, category, date_created)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, goal_id, name, description, deadline,
              priority, category, date_created))
        self.conn.commit()
        return cursor.lastrowid

    def get_tasks_for_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE user_id = ?", user_id)
        rows = cursor.fetchall()
        return [Task(
            row["task_id"], row["user_id"], row["goal_id"],
            row["name"], row["description"], row["deadline"],
            row["priority"], row["category"], row["completed"],
            row["date_created"]
        ) for row in rows]

    def get_task_by_id(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE task_id = ?", task_id)
        row = cursor.fetchone()
        if row:
            task = Task(
                row["task_id"], row["user_id"], row["goal_id"],
                row["name"], row["description"], row["deadline"],
                row["priority"], row["category"], row["completed"],
                row["date_created"]
            )
            if row["date_completed"]:                       # TODO review
                task.mark_complete(row["date_completed"])
            return task
        return None

    def update_task(self, task):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE tasks SET
                name = ?,
                description = ?,
                deadline = ?,
                priority = ?,
                category = ?,
                goal_id = ?
            WHERE task_id = ?
        """, (task.name, task.description, task.deadline,
              task.priority, task.category, task.goal_id,
              task.task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE task_id = ?", task_id)
        self.conn.commit()

    def mark_task_complete(self, task_id, date_completed):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE tasks
            SET completed = 1, date_completed = ?
            WHERE task_id = ?
        """, (date_completed, task_id))
        self.conn.commit()

        task = self.get_task_by_id(task_id)
        history_manager = HistoryManager(self.db)
        history_manager.log_task(task.user_id, task_id, date_completed)

    def mark_task_incomplete(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE tasks
            SET completed = 0, date_completed = NULL
            WHERE task_id = ?
        """, (task_id,))
        self.conn.commit()

        history_manager = HistoryManager(self.db)
        history_manager.remove_task(task_id)
