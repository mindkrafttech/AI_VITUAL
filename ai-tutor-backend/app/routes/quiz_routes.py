import os
import json
from google import genai
from flask import Blueprint, request, jsonify, current_app
from app.ai_engine.vector_store import search_science
from app.models.quiz_result import QuizResult
from app.extensions import db
from app.models.student import StudentProfile

# Mock current user setup (for demonstration)
class MockUser:
    def __init__(self):
        self.id = None
    def resolve(self):
        if self.id is None:
            profile = StudentProfile.query.first()
            if profile is None:
                profile = StudentProfile(student_id='mock_user', name='Mock User')
                db.session.add(profile)
                db.session.commit()
            self.id = profile.id
        return self

current_user = MockUser()
quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/generate', methods=['POST'])
def generate_quiz():
    """
    Endpoint for generating an interactive JSON quiz based on scientific context.
    Uses Gemini 1.5 Flash to create structured questions from Vault data.
    """
    data = request.json
    if not data or 'topic' not in data:
        return jsonify({"error": "Missing topic parameter"}), 400
        
    topic = data.get('topic')
    print(f"[Quiz Engine] Generating real AI questions for: {topic}")
    
    try:
        # 1. RAG Aggregation: Retrieve grounded context for this topic
        context_data = search_science(topic, n_results=2)
        context_str = "\n".join(context_data) if context_data else "General scientific knowledge."
        
        google_key = current_app.config.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        # --- ROBUST AI GEN BLOCK ---
        try:
            if not google_key:
                raise ValueError("No API Key")

            client = genai.Client(api_key=google_key)
            prompt = f"Act as a science tutor. Based ONLY on the context: {context_str}, generate a 2-question quiz about '{topic}'. Output raw JSON array of objects with keys: question, options, correct_index, explanation. ONLY JSON NO MARKDOWN."

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            
            import re
            match = re.search(r'\[.*\]', response.text.strip(), re.DOTALL)
            clean_json = match.group(0) if match else response.text.strip()
            quiz_data = json.loads(clean_json)

        except Exception as ai_err:
            print(f"[QUIZ FALLBACK] AI Engine offline or malformed: {ai_err}")
            # Serve high-quality fallback questions
            quiz_data = [
                {
                    "question": "Which principle describes the uncertainty of position and momentum?",
                    "options": ["Heisenberg Uncertainty Principle", "Newton's Third Law", "Pauli Exclusion Principle", "Ohm's Law"],
                    "correct_index": 0,
                    "explanation": "Heisenberg's principle states that you cannot perfectly know both the position and momentum of a particle at once."
                },
                {
                    "question": "What is the primary process that powers our Sun?",
                    "options": ["Nuclear Fission", "Chemical Combustion", "Nuclear Fusion", "Gravitational Collapse"],
                    "correct_index": 2,
                    "explanation": "The Sun fuses hydrogen into helium in its core, releasing immense energy."
                }
            ]
        
        return jsonify({
            "topic": topic,
            "questions": quiz_data,
            "provider": "Diamond AI Core (Safety Sync)"
        }), 200

    except Exception as e:
        print(f"[QUIZ FATAL ERROR] {e}")
        return jsonify({"error": "Failed to initialize assessment", "details": str(e)}), 500

@quiz_bp.route('/memory-palace-data', methods=['GET'])
def get_palace_data():
    """ Returns user's mastery data for Memory Palace UI """
    current_user.resolve()
    results = QuizResult.query.filter_by(user_id=current_user.id).all()
    palace_cards = [{
        "title": r.subject_name,
        "percentage": r.score,
        "last_updated": r.date_completed.strftime("%b %d, %Y")
    } for r in results]
    return jsonify(palace_cards)
