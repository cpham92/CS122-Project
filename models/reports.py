from abc import ABC, abstractmethod
from collections import Counter

class Report(ABC):
    def __init__(self, history_data):
        self._history_data = history_data

    @abstractmethod
    def generate_text(self):
        """Returns a string summary (for the text box)."""
        pass

    @abstractmethod
    def get_chart_data(self):
        """Returns a dictionary {label: value} (for the Matplotlib graph)."""
        pass

class TaskCompletionReport(Report):
    def generate_text(self):
        return f"Total Tasks Completed: {len(self._history_data)}"

    def get_chart_data(self):
        # Graph: Label "Total", Value = count
        return {"Total": len(self._history_data)}

class UserCompletionReport(Report):
    def generate_text(self):
        user_ids = [h.user_id for h in self._history_data]
        counts = Counter(user_ids)
        text = "User Breakdown:\n"
        for uid, count in counts.items():
            text += f"User {uid}: {count} tasks\n"
        return text

    def get_chart_data(self):
        user_ids = [h.user_id for h in self._history_data]
        counts = Counter(user_ids)
        # Convert keys to strings for graph
        return {f"User {k}": v for k, v in counts.items()}

        # ... existing imports ...

class TaskStatusReport(Report):
    """
    Analyzes ALL tasks (active and finished) to show progress.
    Expects a list of TASK objects, not History objects.
    """
    def generate_text(self):
        total = len(self._history_data) # We reuse the variable name, but this will hold Tasks
        completed = sum(1 for t in self._history_data if t.completed)
        pending = total - completed
        
        return (
            f"=== PROJECT STATUS ===\n"
            f"Total Tasks: {total}\n"
            f"Completed:   {completed}\n"
            f"Pending:     {pending}\n"
        )

    def get_chart_data(self):
        completed = sum(1 for t in self._history_data if t.completed)
        pending = len(self._history_data) - completed
        
        # Returns data for a Bar Chart comparison
        return {
            "Completed": completed,
            "Pending": pending
        }