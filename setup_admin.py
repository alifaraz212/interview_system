"""
Setup script to create an admin account.
Run this once before starting the application.
"""

import sys
from database import Database

def create_admin():
    """Create an admin account"""
    db = Database()
    db.connect()
    
    print("\n" + "="*50)
    print("CREATE ADMIN ACCOUNT")
    print("="*50)
    
    name = input("Enter admin name: ").strip()
    email = input("Enter admin email: ").strip()
    password = input("Enter admin password: ").strip()
    
    # Check if admin already exists
    existing_user = db.get_user_by_email(email)
    if existing_user:
        print("[ERROR] Email already registered")
        db.close()
        return
    
    try:
        admin_id = db.add_user(name, email, password, "admin")
        print(f"[SUCCESS] Admin created!")
        print(f"Admin Email: {email}")
        print(f"Admin Password: {password}")
        print(f"Admin ID: {admin_id}")
    except Exception as e:
        print(f"[ERROR] Failed to create admin: {e}")
    
    db.close()

if __name__ == "__main__":
    create_admin()
