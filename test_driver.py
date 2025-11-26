from db.database import Database
from controllers.user_manager import UserManager
from controllers.goal_manager import GoalManager
from controllers.task_manager import TaskManager
from datetime import datetime

def run_test():
    print("--- STARTING SYSTEM TEST (ID-Based Version) ---")

    # 1. Initialize Database
    db = Database()
    print(f"[OK] Database connected.")

    user_mgr = UserManager(db)
    goal_mgr = GoalManager(db)
    task_mgr = TaskManager(db)

    # 2. Test User Creation
    print("\n--- Testing User ---")
    try:
        # Assuming you are using the UserManager that returns a User object
        user = user_mgr.create_user("test_driver_user", "securePass123")
        if isinstance(user, int): 
            # Fallback if your code returns an ID instead of an object
            user = user_mgr.get_user_by_id(user)
            
        print(f"[OK] Created User: {user.username} (ID: {user.user_id})")
    except Exception as e:
        print(f"[INFO] User might already exist. Fetching...")
        user = user_mgr.get_user_by_username("test_driver_user")
        print(f"[OK] Retrieved User: {user.username} (ID: {user.user_id})")

    # 3. Test Goal Creation (Handling ID return)
    print("\n--- Testing Goal ---")
    # Your code returns an INT (the ID), so we catch it as 'goal_id'
    goal_id = goal_mgr.create_goal(user.user_id, "Learn Py", "Testing backend")
    print(f"[OK] Created Goal ID: {goal_id}")
    
    # Now we fetch the actual object to verify
    goal = goal_mgr.get_goal_by_id(goal_id)
    print(f"[OK] Verified Goal Object Name: {goal.name}")

    # 4. Test Task Creation (Handling ID return)
    print("\n--- Testing Task ---")
    now = datetime.now()
    # Your code returns an INT (the ID)
    task_id = task_mgr.create_task(
        user_id=user.user_id,
        goal_id=goal.goal_id,
        name="Fix Bugs",
        description="Fix the comma bugs",
        deadline="2025-12-31",
        priority="High",
        category="Dev",
        date_created=now
    )
    print(f"[OK] Created Task ID: {task_id}")

    # Fetch object to verify
    task = task_mgr.get_task_by_id(task_id)
    print(f"[OK] Verified Task Object Name: {task.name}")

    # 5. Test Completion & History
    print("\n--- Testing Completion ---")
    task_mgr.mark_task_complete(task.task_id, datetime.now())
    
    # Verify it updated
    updated_task = task_mgr.get_task_by_id(task.task_id)
    if updated_task.completed:
        print(f"[OK] Task marked complete. Date: {updated_task.date_completed}")
    else:
        print("[FAIL] Task was not marked complete.")

if __name__ == "__main__":
    run_test()