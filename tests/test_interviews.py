import pytest
import sys
sys.path.insert(0, '..')
from database import Database

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

def test_get_all_users_by_role(db):
    """Test: Get all users by role"""
    # Add test users
    candidate_id1 = db.add_user("Ali Khan", "ali@email.com", "pass123", "candidate")
    candidate_id2 = db.add_user("Sara Ahmed", "sara@email.com", "pass123", "candidate")
    interviewer_id = db.add_user("John Doe", "john@email.com", "pass123", "interviewer")
    
    # Get all candidates
    candidates = db.get_all_users_by_role("candidate")
    assert len(candidates) == 2
    print(f"Found {len(candidates)} candidates")
    
    # Get all interviewers
    interviewers = db.get_all_users_by_role("interviewer")
    assert len(interviewers) == 1
    print(f"Found {len(interviewers)} interviewer")

def test_add_interview(db):
    """Test: Add interview and link candidate with interviewer"""
    # Create users
    candidate_id = db.add_user("Ali Khan", "ali@email.com", "pass123", "candidate")
    interviewer_id = db.add_user("John Doe", "john@email.com", "pass123", "interviewer")
    
    # Create interview
    interview_id = db.add_interview(candidate_id, interviewer_id, "applied")
    
    assert interview_id is not None
    print(f"Interview created with ID: {interview_id}")
    
    # Verify interview was created by checking directly
    with db.conn.cursor() as cur:
        cur.execute("SELECT * FROM interviews WHERE id = %s", (interview_id,))
        interview = cur.fetchone()
    
    assert interview is not None
    print(f"Interview verified: Candidate {interview[1]} with Interviewer {interview[2]}")

def test_random_interview_assignment(db):
    """Test: Candidate gets randomly assigned to an interviewer"""
    import random
    
    # Create candidate
    candidate_id = db.add_user("Ali Khan", "ali@email.com", "pass123", "candidate")
    
    # Create multiple interviewers
    interviewer_ids = []
    for i in range(3):
        iid = db.add_user(f"Interviewer {i+1}", f"interviewer{i}@email.com", "pass123", "interviewer")
        interviewer_ids.append(iid)
    
    # Get all interviewers
    interviewers = db.get_all_users_by_role("interviewer")
    assert len(interviewers) == 3
    
    # Randomly assign
    random_interviewer = random.choice(interviewers)
    interview_id = db.add_interview(candidate_id, random_interviewer['id'], "applied")
    
    assert interview_id is not None
    print(f"Candidate {candidate_id} assigned to Interviewer {random_interviewer['id']}")
