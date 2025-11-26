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
                 priority, category, date_created, completed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (user_id, goal_id, name, description, deadline,
              priority, category, date_created))
        self.conn.commit()
        
        # returns id rather than task object
        return cursor.lastrowid

    def get_tasks_for_user(self, user_id):
        cursor = self.conn.cursor()
        # FIX: Added comma to make it a tuple (user_id,)
        cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        
        tasks = []
        for row in rows:
            # FIX: Use numeric indices instead of ["name"]
            # FIX: Match the Task.__init__ signature (user_id is first)
            # Row order assumed: 0:id, 1:user, 2:goal, 3:name, 4:desc, 5:deadline, 6:prio, 7:cat, 8:comp, 9:created, 10:completed_date
            t = Task(
                user_id=row[1],
                goal_id=row[2],
                name=row[3],
                description=row[4],
                deadline=row[5],
                priority=row[6],
                category=row[7],
                completed=row[8],
                date_created=row[9],
                date_completed=row[10] if len(row) > 10 else None
            )
            t._task_id = row[0] # Manually set the ID
            tasks.append(t)
        return tasks

    def get_task_by_id(self, task_id):
        cursor = self.conn.cursor()
        # FIX: Added comma 
        cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
        row = cursor.fetchone()
        
        if row:
            # FIX: Correct mapping
            t = Task(
                user_id=row[1],
                goal_id=row[2],
                name=row[3],
                description=row[4],
                deadline=row[5],
                priority=row[6],
                category=row[7],
                completed=row[8],
                date_created=row[9],
                date_completed=row[10] if len(row) > 10 else None
            )
            t._task_id = row[0]
            return t
        return None

    def update_task(self, task):
        # --- NEW SAFETY CHECK ---
        # Make sure task.task.id is set before updating a new task
        if task.task_id is None:
            print("Error: Cannot update a task that has no ID.")
            return
        # ------------------------

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
        cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
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
        if task:
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