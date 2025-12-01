from models.goal import Goal

class GoalManager:
    def __init__(self, db):
        self.conn = db.get_connection()

    def create_goal(self, user_id, name, description):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO goals (user_id, name, description)
            VALUES (?, ?, ?)
        ''', (user_id, name, description))
        self.conn.commit()
        
        # Returning id rather than goal object
        return cursor.lastrowid

    def get_goals_for_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM goals WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            # FIX: Use integer indices (0:id, 1:user_id, 2:name, 3:desc)
            # FIX: Initialize safely and set ID manually
            g = Goal(row[1], row[2], row[3])
            g._goal_id = row[0]
            results.append(g)
        return results

    def get_goal_by_id(self, goal_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM goals WHERE goal_id = ?", (goal_id,))
        row = cursor.fetchone()
        
        if row:
            g = Goal(row[1], row[2], row[3])
            g._goal_id = row[0]
            return g
        return None

    def update_goal(self, goal):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE goals
            SET name = ?, description = ?
            WHERE goal_id = ?
        """, (goal.name, goal.description, goal.goal_id))
        self.conn.commit()

    def delete_goal(self, goal_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM goals WHERE goal_id = ?", (goal_id,))
        self.conn.commit()

    def delete_all_goals_for_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM goals WHERE user_id = ?", (user_id,))
        self.conn.commit()