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


