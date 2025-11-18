from models.user import User

class UserManager:
    def __init__(self, db):
        self.conn = db.get_connection()

    def create_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', (username, password))
        self.conn.commit()
        return cursor.lastrowid

    def get_user_by_username(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", username)
        row = cursor.fetchone()
        if row:
            return User(row["user_id"], row["username"], row["password"])
        return None

    def get_user_by_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", user_id)
        row = cursor.fetchone()
        if row:
            return User(row["user_id"], row["username"], row["password"])
        return None

    def verify_user_credentials(self, username, password):
        user = self.get_user_by_username(username)
        if user and user.verify_password(password):
            return user
        return None

    def delete_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", user_id)
        self.conn.commit()