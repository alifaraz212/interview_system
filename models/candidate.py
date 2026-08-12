from models.user import User

class Candidate(User):
    """Candidate class - inherits from User"""
    
    def __init__(self, user_id, name, email, password, role):
        super().__init__(user_id, name, email, password, role)
    
    def apply_for_interview(self, db):
        """Candidate applies for an interview (randomly assigned to interviewer)"""
        import random
        
        # Get all interviewers
        interviewers = db.get_all_users_by_role("interviewer")
        
        if not interviewers:
            return "No interviewers available"
        
        # Pick random interviewer
        random_interviewer = random.choice(interviewers)
        interviewer_id = random_interviewer['id']
        
        # Create interview
        interview_id = db.add_interview(self.user_id, interviewer_id, "applied")
        
        return f"Applied for interview! Assigned to {random_interviewer['name']} (Interview ID: {interview_id})"
    
    def view_my_interviews(self):
        """Candidate views their interview applications"""
        message = f"{self.name} is viewing their interview applications"
        return message
