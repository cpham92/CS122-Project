# models/user.py
import hashlib

class User:
    def __init__(self, username, password):
        self._user_id = None
        self._username = username
        self._password = self._hash_password(password)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @property
    def user_id(self):
        return self._user_id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = self._hash_password(password)

    def verify_password(self, entered_password):
        hashed_entered_password = hashlib.sha256(entered_password.encode('utf-8')).hexdigest()
        return hashed_entered_password == self._password

if __name__ == '__main__':
    # Example Usage and Testing
    user = User("testuser", "password123")
    print(f"User ID: {user.user_id}")
    print(f"Username: {user.username}")
    print(f"Password (hashed): {user.password}")

    # Verify password
    print(f"Verify 'password123': {user.verify_password('password123')}")  # True
    print(f"Verify 'wrongpassword': {user.verify_password('wrongpassword')}") # False

    # Test setting username
    user.username = "newuser"
    print(f"Username after setting: {user.username}")

    # Test setting password
    user.password = "newpassword"
    print(f"Password after setting: {user.password}")

    print(f"Verify 'newpassword': {user.verify_password('newpassword')}") # True
