class Goal:
    """
    Represents a goal in the goals table.
    """

    def __init__(self, user_id, name, description):
        """
        Initializes a Goal object.

        Args:
            user_id: The ID of the user associated with the goal.
            name: The name of the goal.
            description: The description of the goal.
        """
        self._goal_id = None  # Default to None for autoincrementing primary key
        self._user_id = user_id
        self._name = name
        self._description = description

  # --- Getters and Setters ---

    @property
    def goal_id(self):
  
        return self._goal_id

    @property
    def user_id(self):
   
        return self._user_id

    @property
    def name(self):
     
        return self._name

    @name.setter
    def name(self, value):
        """
        Setter for the name.
        """
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        self._name = value

    @property
    def description(self):
        """
        Getter for the description.
        """
        return self._description

    @description.setter
    def description(self, value):
        """
        Setter for the description.
        """
        if not isinstance(value, str):
            raise TypeError("Description must be a string.")
        self._description = value


if __name__ == '__main__':
    # Example Usage and Testing
    goal1 = Goal(user_id=123, name="Learn Python", description="Start learning Python programming.")
    print(f"Goal ID: {goal1.goal_id}")
    print(f"User ID: {goal1.user_id}")
    print(f"Name: {goal1.name}")
    print(f"Description: {goal1.description}")

    # Setting attributes
    goal1.name = "Learn Python Programming"
    goal1.description = "A more detailed description of the goal."
    print(f"\nUpdated Goal: Name={goal1.name}, Description={goal1.description}, Goal ID={goal1.goal_id}")

    # Example of error handling
    try:
        goal1.name = 123  # Trying to set name to an integer
    except TypeError as e:
        print(f"\nError: {e}")
