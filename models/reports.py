from abc import ABC, abstractmethod
from collections import Counter

class Report(ABC):
    def __init__(self, data):
        self._data = data # list of TASK objects

    @abstractmethod
    def generate_text(self):
        pass

    @abstractmethod
    def get_chart_data(self):
        pass

class TaskStatusReport(Report):
    def generate_text(self):
        total = len(self._data)
        completed = sum(1 for t in self._data if t.completed)
        pending = total - completed
        return f"Total: {total}\nCompleted: {completed}\nPending: {pending}"

    def get_chart_data(self):
        completed = sum(1 for t in self._data if t.completed)
        pending = len(self._data) - completed
        return {"Completed": completed, "Pending": pending}

class PriorityReport(Report):
    def generate_text(self):
        # Count priorities
        priorities = [t.priority for t in self._data]
        counts = Counter(priorities)
        
        text = "=== BY PRIORITY ===\n"
        for p, count in counts.items():
            text += f"{p}: {count}\n"
        return text

    def get_chart_data(self):
        priorities = [t.priority for t in self._data]
        return dict(Counter(priorities))

class CategoryReport(Report):
    def generate_text(self):
        # Handle cases where category is None or empty
        categories = [t.category if t.category else "None" for t in self._data]
        counts = Counter(categories)
        
        text = "=== BY CATEGORY ===\n"
        for c, count in counts.items():
            text += f"{c}: {count}\n"
        return text

    def get_chart_data(self):
        categories = [t.category if t.category else "None" for t in self._data]
        return dict(Counter(categories))