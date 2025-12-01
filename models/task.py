import datetime

class Task:

    def __init__(self, user_id, goal_id=None, name="", description="", deadline=None, priority="Medium", category=None, completed=0, date_created=None, date_completed=None):
        self._task_id = None  # Will be set by the TaskManager
        self._user_id = user_id
        self._goal_id = goal_id
        self._name = name
        self._description = description
        self._deadline = deadline
        self._priority = priority
        self._category = category
        self._completed = completed
        
        # Ensure date_created is a datetime object
        if isinstance(date_created, str):
             #parsing if it comes in as string
             try:
                 self._date_created = datetime.datetime.fromisoformat(date_created)
             except ValueError:
                 self._date_created = datetime.datetime.now()
        else:
            self._date_created = date_created if date_created else datetime.datetime.now()
            
        self._date_completed = date_completed

    # --- Getters and Setters ---
    @property
    def task_id(self):
        return self._task_id

    @property
    def user_id(self):
        return self._user_id

    @property
    def goal_id(self):
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("goal_id must be an integer or None")
        self._goal_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("description must be a string")
        self._description = value

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, value):
        # Allow None or datetime
        if value is not None and not isinstance(value, datetime.datetime):
            raise TypeError("deadline must be a datetime object")
        self._deadline = value

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        if not isinstance(value, str):
            raise TypeError("priority must be a string")
        self._priority = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("category must be a string")
        self._category = value

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, value):
        if not isinstance(value, int):
            raise TypeError("completed must be an integer (0 or 1)")
        self._completed = value

    @property
    def date_created(self):
        return self._date_created

    @property
    def date_completed(self):
        return self._date_completed

   #Task status methods

    def mark_complete(self, date_completed):
        """
        Sets the task as complete and records the completion date.
        """
        if not isinstance(date_completed, datetime.datetime):
            raise TypeError("date_completed must be a datetime object")
        self._completed = 1
        self._date_completed = date_completed

    def mark_incomplete(self):
        self._completed = 0
        self._date_completed = None

    def is_overdue(self):
        # Ensure we have a deadline AND it's a datetime object first
        if self._deadline and isinstance(self._deadline, datetime.datetime) and not self._completed:
            return datetime.datetime.now() > self._deadline
        return False