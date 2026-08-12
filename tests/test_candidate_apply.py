import pytest
import sys
sys.path.insert(0, '..')
from database import Database
from models.candidate import Candidate

@pytest.fixture
def db():
    """Setup: Connect to database and create tables"""
    database = Database()
    database.connect()
    
    # Cleanup before test
    with database.conn.cursor() as cur:
        cur.execute("DELETE FROM interviews")
        cur.execute("DELETE FROM users")
        database.conn.commit()
    
    yield database
    
    # Cleanup after test
    try:
        with database.conn.cursor() as cur:
            cur.execute("DELETE FROM interviews")
            cur.execute("DELETE FROM users")
            database.conn.commit()
    except Exception:
        database.conn.rollback()
    
    database.close()

def test_candidate_apply_for_interview(db):
    """Test: Candidate applies for interview with random assignment"""
    
    # Create candidate
    candidate_id = db.add_user("Ali Khan", "ali@email.com", "pass123", "candidate")
    candidate_data = db.get_user_by_id(candidate_id)
    candidate = Candidate(
        candidate_data['id'],
        candidate_data['name'],
        candidate_data['email'],
        candidate_data['password'],
        candidate_data['role']
    )
    
    # Create interviewers
    for i in range(3):
        db.add_user(f"Interviewer {i+1}", f"interviewer{i}@email.com", "pass123", "interviewer")
    
    # Candidate applies
    result = candidate.apply_for_interview(db)
    print(f"Result: {result}")
    
    assert "Applied for interview" in result
    assert "Assigned to" in result
    assert "Interview ID" in result
    
    # Verify interview was created
    with db.conn.cursor() as cur:
        cur.execute("SELECT * FROM interviews WHERE candidate_id = %s", (candidate_id,))
        interview = cur.fetchone()
    
    assert interview is not None
    print(f"Interview verified in database")

def test_candidate_apply_no_interviewers(db):
    """Test: Candidate tries to apply when no interviewers exist"""
    
    # Create only a candidate
    candidate_id = db.add_user("Ali Khan", "ali@email.com", "pass123", "candidate")
    candidate_data = db.get_user_by_id(candidate_id)
    candidate = Candidate(
        candidate_data['id'],
        candidate_data['name'],
        candidate_data['email'],
        candidate_data['password'],
        candidate_data['role']
    )
    
    # Try to apply
    result = candidate.apply_for_interview(db)
    print(f"Result: {result}")
    
    assert result == "No interviewers available"
