import pytest
import sys
sys.path.insert(0, '..')
from database import Database
from models.candidate import Candidate
from models.interviewer import Interviewer
from models.admin import Admin

@pytest.fixture
def db():
    """Setup: Connect to database and create tables"""
    database = Database()
    database.connect()
    
    # Cleanup before test: Delete all existing data
    with database.conn.cursor() as cur:
        cur.execute("DELETE FROM interviews")
        cur.execute("DELETE FROM users")
        database.conn.commit()
    
    yield database
    
    # Cleanup after test: Delete all data again
    try:
        with database.conn.cursor() as cur:
            cur.execute("DELETE FROM interviews")
            cur.execute("DELETE FROM users")
            database.conn.commit()
    except Exception:
        database.conn.rollback()
    
    database.close()

def test_create_users(db):
    """Test 1: Create users in database"""
    candidate_id = db.add_user("Ali Khan", "ali@email.com", "pass123", "candidate")
    interviewer_id = db.add_user("Sara Ahmed", "sara@email.com", "pass123", "interviewer")
    admin_id = db.add_user("John Admin", "john@email.com", "pass123", "admin")
    
    assert candidate_id is not None
    assert interviewer_id is not None
    assert admin_id is not None
    print(f"Created users - Candidate: {candidate_id}, Interviewer: {interviewer_id}, Admin: {admin_id}")

def test_candidate_methods(db):
    """Test 2: Test Candidate class methods"""
    candidate_id = db.add_user("Ali Khan", "ali@email.com", "pass123", "candidate")
    candidate_data = db.get_user_by_id(candidate_id)
    
    candidate = Candidate(
        candidate_data['id'],
        candidate_data['name'],
        candidate_data['email'],
        candidate_data['password'],
        candidate_data['role']
    )
    
    print(candidate.view_profile())
    print(candidate.apply_for_interview())
    print(candidate.view_my_interviews())
    
    assert candidate.name == "Ali Khan"
    assert candidate.role == "candidate"

def test_login(db):
    """Test 3: Test login with correct and wrong password"""
    candidate_id = db.add_user("Ali Khan", "ali@email.com", "pass123", "candidate")
    candidate_data = db.get_user_by_id(candidate_id)
    
    candidate = Candidate(
        candidate_data['id'],
        candidate_data['name'],
        candidate_data['email'],
        candidate_data['password'],
        candidate_data['role']
    )
    
    # Correct password
    assert candidate.login("pass123") == True
    print("Login with correct password: True")
    
    # Wrong password
    assert candidate.login("wrongpass") == False
    print("Login with wrong password: False")

def test_interviewer_methods(db):
    """Test 4: Test Interviewer class methods"""
    interviewer_id = db.add_user("Sara Ahmed", "sara@email.com", "pass123", "interviewer")
    interviewer_data = db.get_user_by_id(interviewer_id)
    
    interviewer = Interviewer(
        interviewer_data['id'],
        interviewer_data['name'],
        interviewer_data['email'],
        interviewer_data['password'],
        interviewer_data['role']
    )
    
    print(interviewer.view_profile())
    print(interviewer.view_assigned_candidates())
    print(interviewer.mark_interview_completed("Ali Khan"))
    
    assert interviewer.role == "interviewer"

def test_admin_view_all_users(db):
    """Test 5: Admin views all users"""
    db.add_user("Ali Khan", "ali@email.com", "pass123", "candidate")
    db.add_user("Sara Ahmed", "sara@email.com", "pass123", "interviewer")
    admin_id = db.add_user("John Admin", "john@email.com", "pass123", "admin")
    
    admin_data = db.get_user_by_id(admin_id)
    admin = Admin(
        admin_data['id'],
        admin_data['name'],
        admin_data['email'],
        admin_data['password'],
        admin_data['role']
    )
    
    all_users = admin.view_all_users(db)
    print(f"All users: {all_users}")
    
    assert len(all_users) == 3
    print("Admin can see all 3 users")

def test_admin_promote_candidate(db):
    """Test 6: Admin promotes candidate to interviewer"""
    candidate_id = db.add_user("Ali Khan", "ali@email.com", "pass123", "candidate")
    admin_id = db.add_user("John Admin", "john@email.com", "pass123", "admin")
    
    admin_data = db.get_user_by_id(admin_id)
    admin = Admin(
        admin_data['id'],
        admin_data['name'],
        admin_data['email'],
        admin_data['password'],
        admin_data['role']
    )
    
    result = admin.promote_candidate_to_interviewer(db, candidate_id)
    print(result)
    
    updated_user = db.get_user_by_id(candidate_id)
    assert updated_user['role'] == "interviewer"
    print("Candidate promoted to interviewer successfully")

def test_admin_delete_user(db):
    """Test 7: Admin deletes a user"""
    candidate_id = db.add_user("Ali Khan", "ali@email.com", "pass123", "candidate")
    admin_id = db.add_user("John Admin", "john@email.com", "pass123", "admin")
    
    admin_data = db.get_user_by_id(admin_id)
    admin = Admin(
        admin_data['id'],
        admin_data['name'],
        admin_data['email'],
        admin_data['password'],
        admin_data['role']
    )
    
    result = admin.delete_user_account(db, candidate_id)
    print(result)
    
    deleted_user = db.get_user_by_id(candidate_id)
    assert deleted_user is None
    print("User deleted successfully")
