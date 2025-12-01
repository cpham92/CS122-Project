class SettingsManager:
    DEFAULT_COLORS = {
        "high": "#ffcc80",       # orange
        "medium": "#fff6b3",     # yellow
        "low": "#c8f7c5",        # green
        "completed": "#d3d3d3",  # gray
        "overdue": "#ff9999"     # red
    }

    def __init__(self, db):
        self.conn = db.get_connection()

    def get_settings(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM settings WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()

        # If settings exist, return them with defaults
        if row:
            return {
                "high": row["high_color"] or self.DEFAULT_COLORS["high"],
                "medium": row["medium_color"] or self.DEFAULT_COLORS["medium"],
                "low": row["low_color"] or self.DEFAULT_COLORS["low"],
                "completed": row["completed_color"] or self.DEFAULT_COLORS["completed"],
                "overdue": row["overdue_color"] or self.DEFAULT_COLORS["overdue"],
            }

        # No settings
        defaults = self.DEFAULT_COLORS.copy()
        self.save_settings(user_id, defaults)
        return defaults

    def save_settings(self, user_id, colors):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO settings (user_id, high_color, medium_color, low_color,
                                  completed_color, overdue_color)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                high_color      = excluded.high_color,
                medium_color    = excluded.medium_color,
                low_color       = excluded.low_color,
                completed_color = excluded.completed_color,
                overdue_color   = excluded.overdue_color
        """, (
            user_id,
            colors["high"],
            colors["medium"],
            colors["low"],
            colors["completed"],
            colors["overdue"]
        ))
        self.conn.commit()