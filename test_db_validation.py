from database import Database

# Initialize and connect
db = Database()
db.connect()

try:
    print("\n=== Test 1: Add a user ===")
    user_id = db.add_user("TestUser", "test@email.com", "pass123", "candidate")
    print(f"User added with ID: {user_id}")
    
    print("\n=== Test 2: Update role (user exists) ===")
    result = db.update_user_role(user_id, "interviewer")
    print(f"Update result (should be True): {result}")
    
    print("\n=== Test 3: Update role (user does NOT exist) ===")
    result = db.update_user_role(999, "admin")
    print(f"Update result (should be False): {result}")
    
    print("\n=== Test 4: Delete user (user exists) ===")
    result = db.delete_user(user_id)
    print(f"Delete result (should be True): {result}")
    
    print("\n=== Test 5: Delete user (user does NOT exist) ===")
    result = db.delete_user(999)
    print(f"Delete result (should be False): {result}")
    
    print("\n=== Test 6: Get user by ID (exists) ===")
    user = db.get_user_by_id(user_id)
    print(f"User found: {user}")
    
    print("\n=== Test 7: Get user by ID (does NOT exist) ===")
    user = db.get_user_by_id(999)
    print(f"User found: {user}")

finally:
    db.close()
