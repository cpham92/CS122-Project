from db.database import Database
from controllers.user_manager import UserManager
from controllers.goal_manager import GoalManager
from controllers.task_manager import TaskManager
from controllers.history_manager import HistoryManager
from models.reports import TaskCompletionReport, UserCompletionReport
from datetime import datetime

def run_test():
    print("--- STARTING SYSTEM TEST (With Chart Data) ---")

    # 1. Initialize
    db = Database()
    user_mgr = UserManager(db)
    goal_mgr = GoalManager(db)
    task_mgr = TaskManager(db)
    history_mgr = HistoryManager(db)
    print(f"[OK] Database connected.")

    # 2. Setup Data (User -> Goal -> Task)
    # We wrap this in try/except to handle duplicates if you run this multiple times
    try:
        user = user_mgr.create_user("chart_user_01", "pass123")
        if isinstance(user, int): user = user_mgr.get_user_by_id(user)
    except:
        user = user_mgr.get_user_by_username("chart_user_01")
    
    print(f"[OK] User: {user.username} (ID: {user.user_id})")

    goal_id = goal_mgr.create_goal(user.user_id, "Visuals", "Test graphs")
    
    # 3. Create and Complete Multiple Tasks (to make the graph interesting)
    print("\n--- Creating & Completing Tasks ---")
    for i in range(3):
        task_id = task_mgr.create_task(
            user.user_id, goal_id, f"Task {i}", "Desc", 
            datetime(2025, 12, 31), "High", "Dev", datetime.now()
        )
        # Mark complete
        task_mgr.mark_task_complete(task_id, datetime.now())
        # Log to history
        history_mgr.log_task(user.user_id, task_id, datetime.now())
        print(f"[OK] Task {i} completed and logged.")

    # 4. TEST POLYMORPHISM & CHARTS
    print("\n--- Testing Report Polymorphism ---")
    
    # Fetch Data
    history_data = history_mgr.get_history_for_user(user.user_id)
    
    # Create the polymorphic list
    reports = [
        TaskCompletionReport(history_data),
        UserCompletionReport(history_data)
    ]

    for i, report in enumerate(reports):
        print(f"\nReport #{i+1} ({type(report).__name__}):")
        
        # Test 1: Text Output (Old requirement)
        print("  [Text View]:", report.generate_text().replace('\n', ' '))
        
        # Test 2: Chart Data (New requirement)
        data = report.get_chart_data()
        print(f"  [Graph Data]: {data}")
        
        if isinstance(data, dict) and len(data) > 0:
            print("  -> PASSED: Ready for Matplotlib")
        else:
            print("  -> FAILED: No data for graph")

if __name__ == "__main__":
    run_test()