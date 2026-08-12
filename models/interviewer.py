from models.user import User

class Interviewer(User):
    """Interviewer class - inherits from User"""
    
    def __init__(self, user_id, name, email, password, role):
        super().__init__(user_id, name, email, password, role)
    
    def view_assigned_candidates(self):
        """Interviewer views candidates assigned to them"""
        message = f"{self.name} is viewing assigned candidates"
        return message
    
    def mark_interview_completed(self, candidate_name):
        """Interviewer marks an interview as completed"""
        message = f"{self.name} marked interview with {candidate_name} as completed"
        return message
