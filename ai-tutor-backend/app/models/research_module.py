"""
research_module.py
==================
Stores the high-level research modules shown in the Future Tech Vault
carousel slide (Atomic Physics, Bio-Digital Interfaces, Next-Gen MCUs, etc.).

Each module acts as a knowledge "bucket" that scientist entries can link to
via ScientistEntry.module_link.  Progress is tracked per-student through
the `StudentModuleProgress` association table.
"""

from app.extensions import db
from datetime import datetime


# ── Category constants (used as module_category values) ─────────────────────
CATEGORY_SCIENCE    = "science"      # Classic scientists (Faraday, Curie …)
CATEGORY_ATOMIC     = "atomic"       # Nuclear / subatomic physics
CATEGORY_BIO_DIGITAL = "bio_digital" # HMI / BCI / neuro-interfaces
CATEGORY_EMBEDDED   = "embedded"     # Microcontrollers, IoT, embedded AI
CATEGORY_QUANTUM    = "quantum"      # Quantum computing
CATEGORY_CS         = "cs"           # Computer science / software


class ResearchModule(db.Model):
    """
    A high-level study module (e.g. "Atomic Physics", "Bio-Digital Interfaces").
    Scientist entries and quiz results can reference these modules.
    """
    __tablename__ = 'research_modules'

    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(150), nullable=False, unique=True)
    category        = db.Column(db.String(50), nullable=False, default=CATEGORY_SCIENCE)

    # Short tagline shown on the Future Tech carousel card
    tagline         = db.Column(db.String(250), nullable=True)
    # Detailed description shown in the profile overlay
    description     = db.Column(db.Text, nullable=True)

    # Emoji icon used on the module-link-tag pill
    icon            = db.Column(db.String(10), nullable=True)   # e.g. "⚛️"

    # Mastery target (100 for Atomic Physics, 95 for Bio-Digital, etc.)
    mastery_target  = db.Column(db.Float, default=100.0)

    # Is this module visible in the public Knowledge Graph?
    is_active       = db.Column(db.Boolean, default=True)

    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    # Reverse relation: all scientist entries that link to this module
    scientists      = db.relationship(
        'ScientistEntry',
        primaryjoin="foreign(ScientistEntry.module_link) == ResearchModule.title",
        viewonly=True,
        lazy='dynamic'
    )

    def to_dict(self):
        return {
            "id":             self.id,
            "title":          self.title,
            "category":       self.category,
            "tagline":        self.tagline,
            "description":    self.description,
            "icon":           self.icon,
            "mastery_target": self.mastery_target,
            "is_active":      self.is_active,
        }

    def __repr__(self):
        return f"<ResearchModule [{self.category}] {self.title}>"


class StudentModuleProgress(db.Model):
    """
    Association: tracks how far a specific student has progressed
    through a specific research module.
    """
    __tablename__ = 'student_module_progress'

    id              = db.Column(db.Integer, primary_key=True)
    student_id      = db.Column(db.Integer, db.ForeignKey('student_profiles.id'), nullable=False)
    module_id       = db.Column(db.Integer, db.ForeignKey('research_modules.id'), nullable=False)

    current_mastery = db.Column(db.Float, default=0.0)   # 0 – 100
    notes           = db.Column(db.Text, nullable=True)   # AI-generated study notes

    last_updated    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student         = db.relationship('StudentProfile', backref='module_progress')
    module          = db.relationship('ResearchModule', backref='student_progress')

    def to_dict(self):
        return {
            "student_id":      self.student_id,
            "module_id":       self.module_id,
            "module_title":    self.module.title if self.module else None,
            "current_mastery": self.current_mastery,
            "last_updated":    self.last_updated.isoformat() if self.last_updated else None,
        }

    def __repr__(self):
        return f"<StudentModuleProgress student={self.student_id} module={self.module_id} {self.current_mastery}%>"
