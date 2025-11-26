from models.history import History

class HistoryManager:
    def __init__(self, db):
        self.conn = db.get_connection()

    def log_task(self, user_id, task_id, date_completed):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO history (user_id, task_id, date_completed)
            VALUES (?, ?, ?)
        """, (user_id, task_id, date_completed))
        self.conn.commit()
        return cursor.lastrowid

    def get_history_for_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM history WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        
        return [History(
            history_id=row[0], 
            user_id=row[1],
            task_id=row[2], 
            date_completed=row[3]
        ) for row in rows]

    def get_history_for_task(self, task_id):
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM history WHERE task_id = ?", (task_id,))
        rows = cursor.fetchall()
        
        return [History(
            history_id=row[0], 
            user_id=row[1],
            task_id=row[2], 
            date_completed=row[3]
        ) for row in rows]

    # FIX: Renamed this method to match what was called in TaskManager
    def remove_task(self, task_id):
        cursor = self.conn.cursor()

        cursor.execute("DELETE FROM history WHERE task_id = ?", (task_id,))
        self.conn.commit()