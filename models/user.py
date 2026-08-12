class User:
    """Base User class - parent for Candidate, Interviewer, Admin"""
    
    def __init__(self, user_id, name, email, password, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
    
    def login(self, password):
        """Verify password"""
        return self.password == password
    
    def view_profile(self):
        """Display user profile information"""
        profile = f"""
        --- User Profile ---
        ID: {self.user_id}
        Name: {self.name}
        Email: {self.email}
        Role: {self.role}
        """
        return profile
