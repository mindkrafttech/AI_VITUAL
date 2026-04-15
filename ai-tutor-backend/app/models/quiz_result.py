from app.extensions import db
from datetime import datetime

class QuizResult(db.Model):
    __tablename__ = 'quiz_results'

    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100), nullable=False) # e.g., 'React Architecture'
    score = db.Column(db.Float, nullable=False) # The percentage earned
    date_completed = db.Column(db.DateTime, default=datetime.utcnow)
    
    # We associate results with a student profile. The original design
    # referenced a `user` table, which isn't defined anywhere in this codebase,
    # so point the foreign key at the student_profiles table instead.  The
    # field is still named ``user_id`` for compatibility with existing routes.
    user_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id'))

    # convenience relationship so SQLAlchemy can easily join back to the profile
    user = db.relationship('StudentProfile', backref='quiz_results')

    @property
    def mastery_level(self):
        """Calculates the weighted average for the Percentage Badge."""
        # Logic to return the latest or average score for this subject
        return f"{int(self.score)}%"
