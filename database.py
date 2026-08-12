import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
import time

class Database:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv("DB_HOST") or "localhost"
        self.port = int(os.getenv("DB_PORT") or 5433)
        self.database = os.getenv("DB_NAME") or "interview_db"
        self.user = os.getenv("DB_USER") or "interview_user"
        self.password = os.getenv("DB_PASSWORD") or "interview_pass"
        self.conn = None
    
    def connect(self, retries=5):
        """Connect to PostgreSQL with retry logic"""
        for attempt in range(retries):
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
                print("[SUCCESS] Connected to PostgreSQL")
                self.create_tables()
                return
            except Exception as e:
                print(f"Connection attempt {attempt+1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(2)
        
        raise Exception("Failed to connect after retries")
    
    def create_tables(self):
        """Create users and interviews tables"""
        with self.conn.cursor() as cur:
            # Users table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    role VARCHAR(20) NOT NULL
                )
            """)
            
            # Interviews table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS interviews (
                    id SERIAL PRIMARY KEY,
                    candidate_id INT NOT NULL REFERENCES users(id),
                    interviewer_id INT REFERENCES users(id),
                    status VARCHAR(20) DEFAULT 'applied'
                )
            """)
            
            self.conn.commit()
            print("[SUCCESS] Tables created/verified")
    
    def add_user(self, name, email, password, role):
        """Insert a new user and return the ID"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s) RETURNING id",
                (name, email, password, role)
            )
            result = cur.fetchone()
            self.conn.commit()
            return result['id']
    
    def get_user_by_email(self, email):
        """Fetch a user by email"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cur.fetchone()
    
    def get_user_by_id(self, user_id):
        """Fetch a user by ID"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cur.fetchone()
    
    def get_all_users(self):
        """Fetch all users"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users")
            return cur.fetchall()
    
    def update_user_role(self, user_id, new_role):
        """Update a user's role"""
        # Check if user exists
        user = self.get_user_by_id(user_id)
        if not user:
            return False  # User doesn't exist
        
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET role = %s WHERE id = %s",
                (new_role, user_id)
            )
            self.conn.commit()
        return True  # Successfully updated
    
    def delete_user(self, user_id):
        """Delete a user by ID"""
        # Check if user exists
        user = self.get_user_by_id(user_id)
        if not user:
            return False  # User doesn't exist
        
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.conn.commit()
        return True  # Successfully deleted
    
    def get_all_users_by_role(self, role):
        """Fetch all users with a specific role"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE role = %s", (role,))
            return cur.fetchall()
    
    def add_interview(self, candidate_id, interviewer_id, status):
        """Create a new interview"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO interviews (candidate_id, interviewer_id, status) VALUES (%s, %s, %s) RETURNING id",
                (candidate_id, interviewer_id, status)
            )
            result = cur.fetchone()
            self.conn.commit()
            return result['id']
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            print("[SUCCESS] Database connection closed")
