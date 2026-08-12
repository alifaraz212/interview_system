from models.user import User

class Admin(User):
    """Admin class - inherits from User with special privileges"""
    
    def __init__(self, user_id, name, email, password, role):
        super().__init__(user_id, name, email, password, role)
    
    def view_all_users(self, db):
        """Admin views all registered users"""
        users = db.get_all_users()
        return users
    
    def promote_candidate_to_interviewer(self, db, candidate_id):
        """Admin promotes a candidate to interviewer role"""
        result = db.update_user_role(candidate_id, "interviewer")
        if result:
            message = f"{self.name} promoted user {candidate_id} to interviewer"
            return message
        else:
            return f"User {candidate_id} not found"
    
    def delete_user_account(self, db, user_id):
        """Admin deletes a user account"""
        result = db.delete_user(user_id)
        if result:
            message = f"{self.name} deleted user {user_id}"
            return message
        else:
            return f"User {user_id} not found"
