"""
scientist_routes.py
===================
REST API for the Scientist Data Vault + Research Module endpoints.

Prefix registered in __init__.py as: /api/science
"""

from flask import Blueprint, jsonify, request, abort
from app.extensions import db
from app.models.scientist import ScientistEntry
from app.models.research_module import ResearchModule

science_bp = Blueprint('science', __name__)


# ── Scientist Entries ────────────────────────────────────────────────────────

@science_bp.route('/scientists', methods=['GET'])
def list_scientists():
    """
    GET /api/science/scientists
    Returns all scientist vault entries, sorted by mastery descending.
    Optional query param: ?category=atomic
    """
    entries = (
        ScientistEntry.query
        .order_by(ScientistEntry.mastery.desc().nullslast())
        .all()
    )
    return jsonify([e.to_dict() for e in entries]), 200


@science_bp.route('/scientists/<int:entry_id>', methods=['GET'])
def get_scientist(entry_id):
    """GET /api/science/scientists/<id> — single scientist profile."""
    entry = ScientistEntry.query.get_or_404(entry_id)
    return jsonify(entry.to_dict()), 200


@science_bp.route('/scientists', methods=['POST'])
def create_scientist():
    """
    POST /api/science/scientists
    Body JSON: { name, field, bio_short, bio_full, module_link,
                 connection, mastery, student_id }
    """
    data = request.get_json(force=True)
    if not data or not data.get('name'):
        abort(400, description="'name' is required.")

    entry = ScientistEntry(
        name        = data['name'],
        field       = data.get('field', ''),
        bio_short   = data.get('bio_short'),
        bio_full    = data.get('bio_full'),
        module_link = data.get('module_link'),
        connection  = data.get('connection'),
        mastery     = data.get('mastery'),
        student_id  = data.get('student_id'),
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict()), 201


@science_bp.route('/scientists/<int:entry_id>/make_public', methods=['POST'])
def make_public(entry_id):
    """
    POST /api/science/scientists/<id>/make_public
    Marks the scientist entry as published to the Knowledge Graph.
    """
    entry = ScientistEntry.query.get_or_404(entry_id)
    entry.make_public()
    db.session.commit()
    return jsonify({
        "message": f"{entry.name}'s research has been mapped to the Knowledge Graph.",
        "entry": entry.to_dict()
    }), 200


@science_bp.route('/scientists/<int:entry_id>', methods=['PATCH'])
def update_scientist(entry_id):
    """
    PATCH /api/science/scientists/<id>
    Partial update — only fields present in body are modified.
    """
    entry = ScientistEntry.query.get_or_404(entry_id)
    data  = request.get_json(force=True) or {}

    updatable = ['field', 'bio_short', 'bio_full', 'module_link',
                 'connection', 'mastery', 'is_public']
    for field in updatable:
        if field in data:
            setattr(entry, field, data[field])

    db.session.commit()
    return jsonify(entry.to_dict()), 200


# ── Research Modules ─────────────────────────────────────────────────────────

@science_bp.route('/modules', methods=['GET'])
def list_modules():
    """
    GET /api/science/modules
    Returns all research modules. Optional: ?category=atomic
    """
    category = request.args.get('category')
    query = ResearchModule.query.filter_by(is_active=True)
    if category:
        query = query.filter_by(category=category)
    modules = query.order_by(ResearchModule.mastery_target.desc()).all()
    return jsonify([m.to_dict() for m in modules]), 200


@science_bp.route('/modules/<int:module_id>', methods=['GET'])
def get_module(module_id):
    """GET /api/science/modules/<id>"""
    module = ResearchModule.query.get_or_404(module_id)
    return jsonify(module.to_dict()), 200


@science_bp.route('/modules', methods=['POST'])
def create_module():
    """
    POST /api/science/modules
    Body JSON: { title, category, tagline, description, icon, mastery_target }
    """
    data = request.get_json(force=True)
    if not data or not data.get('title'):
        abort(400, description="'title' is required.")

    module = ResearchModule(
        title          = data['title'],
        category       = data.get('category', 'science'),
        tagline        = data.get('tagline'),
        description    = data.get('description'),
        icon           = data.get('icon'),
        mastery_target = data.get('mastery_target', 100.0),
    )
    db.session.add(module)
    db.session.commit()
    return jsonify(module.to_dict()), 201

# ── News Stream ─────────────────────────────────────────────────────────

@science_bp.route('/news', methods=['GET'])
def get_atomic_news():
    """
    GET /api/science/news
    Returns the latest curated news from the Atomic Vault.
    """
    try:
        from app.models.knowledge import NewsArticle
        articles = NewsArticle.query.order_by(NewsArticle.created_at.desc()).limit(10).all()
        return jsonify({
            "status": "success",
            "news": [a.to_dict() for a in articles]
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

