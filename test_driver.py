from db.database import Database
from controllers.user_manager import UserManager
from controllers.goal_manager import GoalManager
from controllers.task_manager import TaskManager
from controllers.history_manager import HistoryManager

# --- UPDATE IMPORTS TO THE NEW CLASSES ---
from models.reports import TaskStatusReport, PriorityReport, CategoryReport
from datetime import datetime

def run_test():
    print("--- STARTING SYSTEM TEST (With New Graphs) ---")

    # 1. Initialize
    db = Database()
    user_mgr = UserManager(db)
    goal_mgr = GoalManager(db)
    task_mgr = TaskManager(db)
    history_mgr = HistoryManager(db)
    print(f"[OK] Database connected.")

    # 2. Setup User
    try:
        user = user_mgr.create_user("graph_user_02", "pass123")
        if isinstance(user, int): user = user_mgr.get_user_by_id(user)
    except:
        user = user_mgr.get_user_by_username("graph_user_02")
    
    print(f"[OK] User: {user.username} (ID: {user.user_id})")

    goal_id = goal_mgr.create_goal(user.user_id, "Visuals", "Test graphs")
    
    # 3. Create Tasks with different Priorities/Categories
    print("\n--- Creating Varied Tasks ---")
    
    # Task 1: High Priority, Dev Category, Completed
    t1_id = task_mgr.create_task(user.user_id, goal_id, "Code Graph", "Desc", datetime(2025,12,31), "High", "Dev", datetime.now())
    task_mgr.mark_task_complete(t1_id, datetime.now())
    
    # Task 2: Medium Priority, Dev Category, Pending
    task_mgr.create_task(user.user_id, goal_id, "Write Tests", "Desc", datetime(2025,12,31), "Medium", "Dev", datetime.now())
    
    # Task 3: Low Priority, School Category, Pending
    task_mgr.create_task(user.user_id, goal_id, "Study Math", "Desc", datetime(2025,12,31), "Low", "School", datetime.now())
    
    print("[OK] Created 3 tasks (1 Done, 2 Pending).")

    # 4. TEST NEW REPORTS
    print("\n--- Testing New Graphic Reports ---")
    
    # IMPORTANT: The new reports analyze TASKS, not History.
    # So we fetch the task list.
    all_tasks = task_mgr.get_tasks_for_user(user.user_id)
    
    # Create the polymorphic list with the NEW classes
    reports = [
        TaskStatusReport(all_tasks),
        PriorityReport(all_tasks),
        CategoryReport(all_tasks)
    ]

    for report in reports:
        # Get the class name
        name = type(report).__name__
        print(f"\nReport Type: {name}")
        
        # Test Text Output
        print("  [Text Summary]:")
        print(report.generate_text().replace('\n', ' | '))
        
        # Test Chart Data
        data = report.get_chart_data()
        print(f"  [Graph Data]: {data}")
        
        if len(data) > 0:
            print("  -> PASSED")
        else:
            print("  -> FAILED (No data)")

if __name__ == "__main__":
    run_test()