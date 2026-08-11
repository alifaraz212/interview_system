from database import Database

# Initialize and connect
db = Database()
db.connect()

try:
    # Test 1: Add a candidate
    print("\n=== Test 1: Add Candidate ===")
    candidate_id = db.add_user("Ali", "ali@email.com", "pass123", "candidate")
    print(f"Candidate added with ID: {candidate_id}")
    
    # Test 2: Add an interviewer
    print("\n=== Test 2: Add Interviewer ===")
    interviewer_id = db.add_user("Sara", "sara@email.com", "pass123", "interviewer")
    print(f"Interviewer added with ID: {interviewer_id}")
    
    # Test 3: Add an admin
    print("\n=== Test 3: Add Admin ===")
    admin_id = db.add_user("John", "john@email.com", "pass123", "admin")
    print(f"Admin added with ID: {admin_id}")
    
    # Test 4: Fetch user by email
    print("\n=== Test 4: Fetch User by Email ===")
    user = db.get_user_by_email("ali@email.com")
    print(f"Found: {dict(user)}")
    
    # Test 5: Get all users
    print("\n=== Test 5: Get All Users ===")
    all_users = db.get_all_users()
    for user in all_users:
        print(f"ID: {user['id']}, Name: {user['name']}, Role: {user['role']}")
    
    # Test 6: Update role
    print("\n=== Test 6: Update User Role ===")
    db.update_user_role(candidate_id, "interviewer")
    updated_user = db.get_user_by_id(candidate_id)
    print(f"Updated {updated_user['name']}'s role to: {updated_user['role']}")
    
    # Test 7: Delete user (Admin action)
    print("\n=== Test 7: Delete User (Admin action) ===")
    db.delete_user(candidate_id)
    print(f"Deleted user with ID: {candidate_id}")
    
    # Verify deletion
    print("\n=== Verify Deletion ===")
    remaining_users = db.get_all_users()
    print(f"Remaining users: {len(remaining_users)}")
    for user in remaining_users:
        print(f"ID: {user['id']}, Name: {user['name']}, Role: {user['role']}")

finally:
    db.close()
