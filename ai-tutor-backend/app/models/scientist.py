"""
scientist.py
============
Stores the "Scientist Data Vault" entries from the Memory Palace.
Each row represents one scientist card with their field, mastery score,
biographical notes, knowledge-graph connection text, and public visibility.
"""

from app.extensions import db
from datetime import datetime


class ScientistEntry(db.Model):
    __tablename__ = 'scientist_entries'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(120), nullable=False, unique=True)
    field         = db.Column(db.String(120), nullable=False)

    # Short paragraph shown on the card
    bio_short     = db.Column(db.Text, nullable=True)
    # Full biography shown in the profile overlay
    bio_full      = db.Column(db.Text, nullable=True)

    # Which learning module this scientist maps to
    module_link   = db.Column(db.String(120), nullable=True)  # e.g. "Quantum Computing"
    # The AI mentor message shown when data is shared
    connection    = db.Column(db.Text, nullable=True)

    # Mastery percentage (0-100). NULL means "goal not yet set"
    mastery       = db.Column(db.Float, nullable=True)
    # True = visible in public Knowledge Graph
    is_public     = db.Column(db.Boolean, default=False, nullable=False)

    # Timestamps
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    published_at  = db.Column(db.DateTime, nullable=True)   # set when Make Public is clicked

    # Foreign key — which student "owns" this entry
    student_id    = db.Column(
        db.Integer,
        db.ForeignKey('student_profiles.id'),
        nullable=True
    )
    student       = db.relationship('StudentProfile', backref='scientist_entries')

    def make_public(self):
        """Mark the entry as published to the Knowledge Graph."""
        self.is_public    = True
        self.published_at = datetime.utcnow()

    def to_dict(self):
        return {
            "id":           self.id,
            "name":         self.name,
            "field":        self.field,
            "bio_short":    self.bio_short,
            "bio_full":     self.bio_full,
            "module_link":  self.module_link,
            "connection":   self.connection,
            "mastery":      self.mastery,
            "is_public":    self.is_public,
            "created_at":   self.created_at.isoformat() if self.created_at else None,
            "published_at": self.published_at.isoformat() if self.published_at else None,
        }

    def __repr__(self):
        return f"<ScientistEntry {self.name} ({self.mastery}%)>"
