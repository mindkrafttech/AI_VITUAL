from flask import Blueprint, request, jsonify
from app.ai_engine.tutor_logic import generate_tutor_response, generate_research_summary
from app.ai_engine.vector_store import search_science
import random

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/query', methods=['POST'])
def query_tutor():
    """
    Endpoint for the React/HTML frontend to talk to the AI Tutor.
    Expects JSON: { "question": "What is quantum entanglement?", "context": "physics" }
    """
    data = request.json
    if not data or not 'question' in data:
        return jsonify({"error": "Missing question parameter"}), 400
        
    question = data.get('question')
    student_context = data.get('context', 'general')
    
    # Send the question to the AI logic engine (which uses RAG under the hood)
    response_data = generate_tutor_response(question, student_context)
    
    return jsonify(response_data), 200

@ai_bp.route('/research', methods=['POST'])
def research_topic():
    """
    Specifically for the 'Quick Research' bullet points.
    JSON: { "topic": "Quantum Mechanics" }
    """
    data = request.json
    if not data or not 'topic' in data:
        return jsonify({"error": "Missing topic"}), 400
    
    topic = data.get('topic')
    response_data = generate_research_summary(topic)
    return jsonify(response_data), 200

@ai_bp.route('/recommend-next/<topic>', methods=['GET'])
def recommend_next_concepts(topic):
    """
    Queries the Knowledge Vault (ChromaDB) to find concepts conceptually related
    to the current active topic. These are then visualized in the frontend interactive graph.
    """
    try:
        # Search the knowledge vault for the active topic to pull related documents
        context = search_science(f"What is related to {topic}?", n_results=1)
        
        # If the DB is completely empty or has no matches, fallback to mock nodes
        if not context:
             related_concepts = ["Physics", "Mathematics", "Quantum Mechanics", "Calculus", "Data Science"]
        else:
             # Very basic mockup logic to extract concepts from DB sentences (in a real app you'd run this string through an NER pipeline or LLM for strict noun phrases)
             # Here we split words, filter out small words, and optionally select 5 random terms to act as "nodes"
             words = [w.strip('.,?!').title() for w in str(context).split() if len(w) > 4]
             # Deduplicate and cap at 5
             related_concepts = list(set(words))[:5]
             
             if len(related_concepts) < 5:
                  # Pad if needed
                  related_concepts.extend(["Physics", "Calculus", "Chemistry", "Biology", "Geometry"][:5-len(related_concepts)])

        # Convert simple string concepts into structured React-style nodes with mock positions
        related_nodes = []
        for i, concept in enumerate(related_concepts):
             related_nodes.append({
                 "id": i,
                 "label": concept,
                 "x": 100 + (i * 150), # Mock positioning for strict React integration
                 "y": 200 + (i % 2 * 100)
             })

        return jsonify({
            "activeTopic": topic,
            "relatedConcepts": related_nodes
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/save-research', methods=['POST'])
def save_research():
    """
    Saves a specific Scientist data point to the database, persisting
    it to the Research Archive / Memory Palace interface.
    """
    from app.extensions import db
    from app.models.knowledge import Scientist
    
    data = request.json
    if not data or not data.get('name'):
         return jsonify({"error": "Missing scientist name"}), 400
         
    try:
        new_entry = Scientist(
            name=data['name'],
            field=data.get('field', 'General Science'),
            research_notes=data.get('notes', 'No notes provided')
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"status": "success", "message": "Research saved to Vault"}), 201
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/upload', methods=['POST'])
def upload_lesson():
    """
    High-Fidelity Science Upload:
    Takes manual lesson text from the 'Teach Diamond' button and instills
    it into the ChromaDB Knowledge Vault.
    """
    import time
    from app.ai_engine.vector_store import add_scientific_data
    
    data = request.json
    if not data or not data.get('text'):
        return jsonify({"error": "No lesson text provided"}), 400
    
    lesson_text = data.get('text')
    lesson_id = f"user_lesson_{int(time.time())}"
    
    try:
        # Add to the Vector Store for RAG retrieval
        add_scientific_data(lesson_id, lesson_text, {"source": "manual_upload", "type": "lesson"})
        return jsonify({
            "status": "success", 
            "message": "Lesson committed to long-term memory.",
            "id": lesson_id
        }), 200
    except Exception as e:
        print(f"[UPLOAD ERROR] {e}")
        return jsonify({"error": "Failed to instill knowledge"}), 500
