from models.user import User

class Candidate(User):
    """Candidate class - inherits from User"""
    
    def __init__(self, user_id, name, email, password, role):
        super().__init__(user_id, name, email, password, role)
    
    def apply_for_interview(self):
        """Candidate applies for an interview"""
        message = f"{self.name} has applied for an interview"
        return message
    
    def view_my_interviews(self):
        """Candidate views their interview applications"""
        message = f"{self.name} is viewing their interview applications"
        return message
