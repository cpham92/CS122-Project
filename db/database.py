import sqlite3
from pathlib import Path

DB_PATH = Path("db/taskfriend.db")

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # --- USER TABLE ---
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # --- GOAL TABLE ---
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
        ''')

        # --- TASK TABLE ---
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                goal_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                deadline TEXT,
                priority TEXT NOT NULL CHECK(priority IN ('Low', 'Medium', 'High')),
                category TEXT,
                completed INTEGER NOT NULL DEFAULT 0 CHECK(completed IN (0, 1)),
                date_created TEXT NOT NULL DEFAULT (datetime('now')),
                date_completed TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                FOREIGN KEY(goal_id) REFERENCES goals(goal_id)
                    ON DELETE SET NULL
                    ON UPDATE CASCADE
            )
        ''')

        # --- HISTORY TABLE ---
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_id INTEGER NOT NULL,
                date_completed TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY(user_id) REFERENCES users(user_id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                FOREIGN KEY(task_id) REFERENCES tasks(task_id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
        ''')

        # --- SETTINGS TABLE ---
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                user_id INTEGER PRIMARY KEY,
                high_color TEXT DEFAULT '#ffcc80',
                medium_color TEXT DEFAULT '#fff6b3',
                low_color TEXT DEFAULT '#c8f7c5',
                completed_color TEXT DEFAULT '#d3d3d3',
                overdue_color TEXT DEFAULT '#ff9999',
                FOREIGN KEY (user_id) REFERENCES users(user_id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE  
            )
        ''')
        self.conn.commit()

    def get_connection(self):
        return self.conn