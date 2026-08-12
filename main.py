import sys
from database import Database
from models.candidate import Candidate
from models.interviewer import Interviewer
from models.admin import Admin

def show_main_menu():
    """Display login/signup menu"""
    print("\n" + "="*50)
    print("INTERVIEW PLATFORM")
    print("="*50)
    print("1. Login")
    print("2. Signup")
    print("3. Exit")
    print("="*50)

def show_candidate_menu():
    """Display candidate menu"""
    print("\n" + "-"*50)
    print("CANDIDATE MENU")
    print("-"*50)
    print("1. Apply for Interview")
    print("2. View My Interviews")
    print("3. Logout")
    print("-"*50)

def show_interviewer_menu():
    """Display interviewer menu"""
    print("\n" + "-"*50)
    print("INTERVIEWER MENU")
    print("-"*50)
    print("1. View Assigned Candidates")
    print("2. Mark Interview Completed")
    print("3. Logout")
    print("-"*50)

def show_admin_menu():
    """Display admin menu"""
    print("\n" + "-"*50)
    print("ADMIN MENU")
    print("-"*50)
    print("1. View All Users")
    print("2. Delete User Account")
    print("3. Logout")
    print("-"*50)

def login(db):
    """Handle user login"""
    print("\n--- LOGIN ---")
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()
    
    # Verify user exists
    user_data = db.get_user_by_email(email)
    
    if not user_data:
        print("[ERROR] User not found")
        return None
    
    # Verify password
    if user_data['password'] != password:
        print("[ERROR] Invalid password")
        return None
    
    print(f"[SUCCESS] Welcome, {user_data['name']}!")
    return user_data

def signup(db):
    """Handle user signup"""
    print("\n--- SIGNUP ---")
    print("Select role:")
    print("1. Candidate")
    print("2. Interviewer")
    role_choice = input("Enter choice: ").strip()
    
    if role_choice == "1":
        role = "candidate"
    elif role_choice == "2":
        role = "interviewer"
    else:
        print("[ERROR] Invalid choice")
        return None
    
    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()
    
    # Check if email already exists
    existing_user = db.get_user_by_email(email)
    if existing_user:
        print("[ERROR] Email already registered")
        return None
    
    try:
        user_id = db.add_user(name, email, password, role)
        print(f"[SUCCESS] Account created as {role}! Please login.")
        return None
    except Exception as e:
        print(f"[ERROR] Signup failed: {e}")
        return None

def handle_candidate(candidate_obj, db):
    """Handle candidate actions"""
    while True:
        show_candidate_menu()
        choice = input("Enter choice: ").strip()
        
        if choice == "1":
            # Apply for interview
            result = candidate_obj.apply_for_interview(db)
            print(f"\n{result}")
            
            # Ask if they want to apply again
            apply_again = input("Apply for another interview? (yes/no): ").strip().lower()
            if apply_again != "yes":
                continue
        
        elif choice == "2":
            # View my interviews
            print("\n--- MY INTERVIEWS ---")
            with db.conn.cursor() as cur:
                cur.execute("""
                    SELECT i.id, u.name as interviewer_name, i.status
                    FROM interviews i
                    JOIN users u ON i.interviewer_id = u.id
                    WHERE i.candidate_id = %s
                """, (candidate_obj.user_id,))
                interviews = cur.fetchall()
            
            if not interviews:
                print("No interviews yet")
            else:
                for interview in interviews:
                    print(f"Interview ID: {interview[0]}, Interviewer: {interview[1]}, Status: {interview[2]}")
        
        elif choice == "3":
            print("[INFO] Logged out")
            break
        
        else:
            print("[ERROR] Invalid choice")

def handle_interviewer(interviewer_obj, db):
    """Handle interviewer actions"""
    while True:
        show_interviewer_menu()
        choice = input("Enter choice: ").strip()
        
        if choice == "1":
            # View assigned candidates
            print("\n--- ASSIGNED CANDIDATES ---")
            with db.conn.cursor() as cur:
                cur.execute("""
                    SELECT i.id, u.name as candidate_name, i.status
                    FROM interviews i
                    JOIN users u ON i.candidate_id = u.id
                    WHERE i.interviewer_id = %s
                """, (interviewer_obj.user_id,))
                interviews = cur.fetchall()
            
            if not interviews:
                print("No assigned candidates")
            else:
                for interview in interviews:
                    print(f"Interview ID: {interview[0]}, Candidate: {interview[1]}, Status: {interview[2]}")
        
        elif choice == "2":
            # Mark interview completed
            interview_id = input("Enter interview ID: ").strip()
            try:
                with db.conn.cursor() as cur:
                    cur.execute(
                        "UPDATE interviews SET status = %s WHERE id = %s AND interviewer_id = %s",
                        ("completed", interview_id, interviewer_obj.user_id)
                    )
                    db.conn.commit()
                print("[SUCCESS] Interview marked as completed")
            except Exception as e:
                print(f"[ERROR] {e}")
        
        elif choice == "3":
            print("[INFO] Logged out")
            break
        
        else:
            print("[ERROR] Invalid choice")

def handle_admin(admin_obj, db):
    """Handle admin actions"""
    while True:
        show_admin_menu()
        choice = input("Enter choice: ").strip()
        
        if choice == "1":
            # View all users
            print("\n--- ALL USERS ---")
            all_users = admin_obj.view_all_users(db)
            for user in all_users:
                print(f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}, Role: {user['role']}")
        
        elif choice == "2":
            # Delete user account
            email = input("Enter user email to delete: ").strip()
            user = db.get_user_by_email(email)
            
            if not user:
                print("[ERROR] User not found")
            else:
                result = admin_obj.delete_user_account(db, user['id'])
                print(f"{result}")
        
        elif choice == "3":
            print("[INFO] Logged out")
            break
        
        else:
            print("[ERROR] Invalid choice")

def main():
    """Main application loop"""
    db = Database()
    db.connect()
    
    try:
        while True:
            show_main_menu()
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                # Login
                user_data = login(db)
                if user_data:
                    # Create appropriate object based on role
                    if user_data['role'] == "candidate":
                        user_obj = Candidate(
                            user_data['id'],
                            user_data['name'],
                            user_data['email'],
                            user_data['password'],
                            user_data['role']
                        )
                        handle_candidate(user_obj, db)
                    
                    elif user_data['role'] == "interviewer":
                        user_obj = Interviewer(
                            user_data['id'],
                            user_data['name'],
                            user_data['email'],
                            user_data['password'],
                            user_data['role']
                        )
                        handle_interviewer(user_obj, db)
                    
                    elif user_data['role'] == "admin":
                        user_obj = Admin(
                            user_data['id'],
                            user_data['name'],
                            user_data['email'],
                            user_data['password'],
                            user_data['role']
                        )
                        handle_admin(user_obj, db)
            
            elif choice == "2":
                # Signup
                signup(db)
            
            elif choice == "3":
                # Exit
                print("[INFO] Goodbye!")
                break
            
            else:
                print("[ERROR] Invalid choice")
    
    finally:
        db.close()

if __name__ == "__main__":
    main()
