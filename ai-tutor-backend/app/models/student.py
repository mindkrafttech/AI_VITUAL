from app.extensions import db
from datetime import datetime

class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    
    # Persistent Memory: Tracking struggles and mastered topics
    struggled_topics = db.Column(db.JSON, default=list) # e.g., ["Newton's Second Law"]
    mastered_topics = db.Column(db.JSON, default=list)  # e.g., ["Quantum Entanglement"]
    
    # Store chat history or contextual memory
    last_interaction = db.Column(db.DateTime, default=datetime.utcnow)
    learning_style_preference = db.Column(db.String(50), default="visual")
    
    def __repr__(self):
        return f"<StudentProfile {self.student_id}>"
