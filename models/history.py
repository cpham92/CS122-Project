from datetime import datetime
from collections import Counter
from abc import ABC, abstractmethod  # <--- ADDED THIS

class History:
    """
     a single history entry related to a task's completion.
    """
    def __init__(self, history_id, user_id, task_id, date_completed):
        self._history_id = history_id
        self._user_id = user_id
        self._task_id = task_id
        self._date_completed = date_completed

    # Getters
    @property
    def history_id(self):
        return self._history_id

    @property
    def user_id(self):
        return self._user_id

    @property
    def task_id(self):
        return self._task_id

    @property
    def date_completed(self):
        return self._date_completed


class Report(ABC):  # <---  INHERIT FROM ABC, Abstract report class for inheritance

    """
    Abstract base class for generating reports from history data.
    """
    def __init__(self, history_data):
        #list of History objects to analyze.
        
        self._history_data = history_data

    @abstractmethod
    def generate_report(self):
        """
        subclasses must implement this
        """
        pass


class TaskCompletionReport(Report):
    def generate_report(self):
        print(f"Generating Task Completion Report for {len(self._history_data)} items...")
        # Example logic: Simply count them for now
        return len(self._history_data)


class UserCompletionReport(Report):
    def generate_report(self):
        print("Generating User Completion Report...")
        # Placeholder logic
        pass