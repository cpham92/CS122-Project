from models.user import User

class UserManager:
    def __init__(self, db):
        self.conn = db.get_connection()

    def create_user(self, username, password):
        # FIX: Create the User object first.
        # This triggers the __init__ method which hashes the password for us
        new_user = User(username, password)
        
        cursor = self.conn.cursor()
        try:
            # Save new_user.password (the hash), not the raw 'password' variable
            cursor.execute('''
                INSERT INTO users (username, password)
                VALUES (?, ?)
            ''', (new_user.username, new_user.password))
            self.conn.commit()
            
            # Update the ID and return the full object
            new_user._user_id = cursor.lastrowid
            return new_user
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def get_user_by_username(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_user(row)
        return None

    def get_user_by_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_user(row)
        return None

    def _row_to_user(self, row):
        """Helper to convert a DB row to a User object safely."""
        # row[0]=id, row[1]=username, row[2]=password_hash
        
        # FIX : Prevent Double Hashing.
        # We pass a dummy "" as password so __init__ doesn't hash the already-hashed DB value.
        user = User(row[1], "") 
        
        # Manually inject the real data
        user._user_id = row[0]
        user._password = row[2] # This is the correct hash from DB
        return user

    def verify_user_credentials(self, username, entered_password):
        user = self.get_user_by_username(username)
        
        # user.verify_password hashes 'entered_password' and compares it to user._password
        if user and user.verify_password(entered_password):
            return user
        return None

    def delete_user(self, user_id):
        cursor = self.conn.cursor()

        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        self.conn.commit()