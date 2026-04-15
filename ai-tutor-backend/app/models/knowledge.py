from app.extensions import db
from datetime import datetime

class ScientificFormula(db.Model):
    """
    Structured Facts (PostgreSQL)
    Stores rigid, absolute mathematical and scientific formulas.
    """
    __tablename__ = 'scientific_formulas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False) # e.g. "Newton's Second Law"
    equation = db.Column(db.String(100), nullable=False) # e.g. "F = ma"
    subject = db.Column(db.String(50), nullable=False) # e.g. "Physics"
    variables_json = db.Column(db.JSON, nullable=True) # e.g. {"F": "Force", "m": "mass", "a": "acceleration"}

    def __repr__(self):
        return f"<Formula {self.name}: {self.equation}>"


class ScientificConstant(db.Model):
    """
    Structured Facts (PostgreSQL)
    Stores rigid scientific constants (Gravity, Speed of Light, Planck's)
    """
    __tablename__ = 'scientific_constants'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), unique=True, nullable=False) # e.g. "c"
    name = db.Column(db.String(100), nullable=False) # e.g. "Speed of Light"
    value = db.Column(db.Float, nullable=False) # e.g. 299792458
    unit = db.Column(db.String(50), nullable=False) # e.g. "m/s"
    
    def __repr__(self):
        return f"<Constant {self.symbol} = {self.value}>"


class MediaAsset(db.Model):
    """
    Media Assets Layer (AWS S3 / Cloudinary Linker)
    Maps a scientific topic to external 3D models or video lessons.
    """
    __tablename__ = 'media_assets'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False) # e.g. "Mitochondria"
    asset_type = db.Column(db.String(50), nullable=False) # e.g. "3D_MODEL", "VIDEO", "ANATOMY_DIAGRAM"
    s3_url = db.Column(db.String(500), nullable=False) # e.g. "https://s3.aws.com/science-assets/mitochondria_3d.gltf"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<MediaAsset {self.asset_type} for {self.topic}>"

class Scientist(db.Model):
    """
    Scientist Data Vault
    Stores saved research entities from the Memory Palace / Knowledge Vault.
    """
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # e.g., Michael Faraday
    field = db.Column(db.String(100)) # e.g., Electromagnetism
    research_notes = db.Column(db.Text) # "Research" data to save
    mastery_score = db.Column(db.Integer, default=0) # Links to Percentage Badge

    def __repr__(self):
        return f"<Scientist {self.name} - {self.field}>"

class NewsArticle(db.Model):
    """
    Atomic Vault Pipeline Data Model
    Stores real-time scientific news scraped from external sources like Phys.org.
    """
    __tablename__ = 'news_articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), default="Atomic Future")
    timestamp = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "timestamp": self.timestamp,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<NewsArticle {self.title[:20]}...>"
