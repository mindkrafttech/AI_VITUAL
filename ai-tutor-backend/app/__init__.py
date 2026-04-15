from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Critical: Load environment variables from .env file
load_dotenv()

from app.extensions import db
from celery_worker import celery_app
from datetime import datetime


def _seed_research_modules():
    """
    Idempotent seed: inserts default ResearchModule rows only if the
    table is empty.  Called automatically inside create_app().
    """
    from app.models.research_module import (
        ResearchModule,
        CATEGORY_QUANTUM, CATEGORY_ATOMIC, CATEGORY_BIO_DIGITAL,
        CATEGORY_EMBEDDED, CATEGORY_SCIENCE, CATEGORY_CS,
    )

    if ResearchModule.query.count() > 0:
        return  # Already seeded — skip

    defaults = [
        ResearchModule(
            title="Quantum Computing",
            category=CATEGORY_QUANTUM,
            icon="⚛️",
            tagline="Superposition, entanglement, and qubit design.",
            description="Covers qubits, quantum gates, Grover/Shor algorithms, "
                        "and the connection between Hawking Radiation and qubit decoherence.",
            mastery_target=100.0,
        ),
        ResearchModule(
            title="Atomic Physics",
            category=CATEGORY_ATOMIC,
            icon="🌟",
            tagline="Subatomic particles, nuclear fusion, and quantum fields.",
            description="Deep dive into quarks, leptons, bosons, and the fusion "
                        "reactions that power stars. 2026 mastery target.",
            mastery_target=100.0,
        ),
        ResearchModule(
            title="Bio-Digital Interfaces",
            category=CATEGORY_BIO_DIGITAL,
            icon="🧠",
            tagline="HMI, BCI, and neural signal processing.",
            description="EEG pipelines, human-machine interface design, and "
                        "real-time biosignal processing for medical devices.",
            mastery_target=95.0,
        ),
        ResearchModule(
            title="Smart Patient Monitor",
            category=CATEGORY_EMBEDDED,
            icon="📡",
            tagline="ESP32-S3 + Raspberry Pi 5 embedded AI stack.",
            description="ESP32-S3 handles analog biosignal acquisition; "
                        "RPi 5 runs on-device AI inference for anomaly detection.",
            mastery_target=90.0,
        ),
        ResearchModule(
            title="Applied Mathematics",
            category=CATEGORY_SCIENCE,
            icon="📐",
            tagline="Calculus, linear algebra, and physics engines.",
            description="Newton's laws, integral/differential calculus, and "
                        "their direct application in game physics and simulations.",
            mastery_target=95.0,
        ),
        ResearchModule(
            title="Systems Programming",
            category=CATEGORY_CS,
            icon="🛰️",
            tagline="Relativity, GPS algorithms, and low-level CS.",
            description="How Einstein's special relativity requires time-correction "
                        "in GPS satellite software. C, Rust, and OS fundamentals.",
            mastery_target=90.0,
        ),
    ]

    db.session.add_all(defaults)
    db.session.commit()
    print(f"[seed] Inserted {len(defaults)} default ResearchModule rows.")


def _seed_news_articles():
    """
    Seeds the Atomic Vault with 2026 milestones if the table is empty.
    """
    from app.models.knowledge import NewsArticle
    if NewsArticle.query.count() > 0:
        return

    milestones = [
        NewsArticle(
            title="Fusion Stabilization: China's EAST (Artificial Sun) Milestone",
            content="Maintain plasma stability at extreme densities using AI-driven magnetic confinement. 2026 breakthrough.",
            category="Atomic Future",
            timestamp=datetime.now().strftime("%H:%M")
        ),
        NewsArticle(
            title="Nikola Tesla Resonance: High-Frequency Wireless HMI",
            content="Integration of resonant inductive coupling for high-fidelity wireless energy in biosensors.",
            category="Atomic Future",
            timestamp=datetime.now().strftime("%H:%M")
        ),
        NewsArticle(
            title="Hidden Quantum Geometry: Steering Electrons like Gravity",
            content="Experimental observation of the 'Quantum Metric' which dictates electron behavior in topological insulators.",
            category="Atomic Future",
            timestamp=datetime.now().strftime("%H:%M")
        )
    ]
    db.session.add_all(milestones)
    db.session.commit()
    print(f"[seed] Inserted {len(milestones)} curated 2026 milestones.")


def create_app():
    # Detect the frontend directory (Diamond Dashboard)
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'diamond-dashboard')
    
    app = Flask(__name__, static_folder=frontend_path, static_url_path='')
    CORS(app) # Allow frontend dashboard to communicate with backend

    app.config.from_pyfile('../config.py')
    
    # Initialize Persistent Data Layer (PostgreSQL/SQLite)
    db.init_app(app)
    
    # Initialize Asynchronous Tasks (Celery/Redis)
    celery_app.conf.update(app.config)

    with app.app_context():
        # Models must be imported before creating all tables
        from app.models import student
        from app.models import knowledge
        from app.models import quiz_result
        from app.models import scientist          # ScientistEntry
        from app.models import research_module    # ResearchModule, StudentModuleProgress
        db.create_all()

        # Seed default data if requested
        _seed_research_modules()
        _seed_news_articles()

        # [AUTO-DEPLOY] Sync the latest AI Avatar to the dashboard folder
        try:
            import glob, shutil
            # [FORCE-CLEANUP] Remove legacy identities to fulfill 'delect' request
            brain_dir = r"C:\Users\santh\.gemini\antigravity\brain\58a52468-daea-496a-b5ef-0fa5c4a60ff9"
            all_pngs = glob.glob(os.path.join(brain_dir, "*.png"))
            
            # The only identity we want to keep
            elite_id = "premium_waving_hologram_mentor_obsidian_v1"
            
            for f in all_pngs:
                if elite_id not in os.path.basename(f):
                    try:
                        os.remove(f)
                        print(f"[BRAIN-CLEANUP] Delected old identity: {os.path.basename(f)}")
                    except: pass
            
            # [ELITE-SYNC] Deploy the premium identity
            elite_files = glob.glob(os.path.join(brain_dir, f"{elite_id}*.png"))
            if elite_files:
                latest_brain_file = max(elite_files, key=os.path.getctime)
                dest = os.path.join(frontend_path, "avatar_v3.png")
                # Force delete the destination too to ensure overwrite
                if os.path.exists(dest): os.remove(dest)
                shutil.copy2(latest_brain_file, dest)
                print(f"[BRAIN-SYNC] Elite Identity V3 Deployed: {os.path.basename(latest_brain_file)}")
        except Exception as e:
            print(f"[BRAIN-SYNC] Identity deployment failed: {e}")

    @app.route('/avatar', methods=['GET'])
    def serve_avatar():
        """ Serves the Elite high-fidelity identity from the session Brain """
        import glob
        try:
            # Dynamically prioritize the Elite Waving Identity 
            brain_dir = r"C:\Users\santh\.gemini\antigravity\brain\58a52468-daea-496a-b5ef-0fa5c4a60ff9"
            pattern = os.path.join(brain_dir, "premium_waving_hologram_mentor_obsidian_*.png")
            elite_files = glob.glob(pattern)
            
            if elite_files:
                latest_file = max(elite_files, key=os.path.getctime)
            else:
                # Fallback to any PNG
                pattern = os.path.join(brain_dir, "*.png")
                files = glob.glob(pattern)
                latest_file = max(files, key=os.path.getctime) if files else None

            if latest_file:
                print(f"[BRAIN-SYNC] Serving Elite Scan V3: {os.path.basename(latest_file)}") 
                file_dir = os.path.dirname(latest_file)
                file_name = os.path.basename(latest_file)
                response = make_response(send_from_directory(file_dir, file_name))
                response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                return response
                
            print("[BRAIN-SYNC] Warning: Identity Vault Empty.")
            print("[BRAIN-SYNC] Warning: No identity found in brain vault.")
        except Exception as e:
            print(f"[BRAIN-SYNC] Error serving identity: {e}")
        return jsonify({"error": "Avatar not found"}), 404

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "service": "Diamond Tutor AI Backend", "db": "connected"}), 200

    @app.route('/')
    def index():
        """ Serves the Diamond Dashboard Front-end """
        return send_from_directory(app.static_folder, 'index.html')

    # Import and register blueprints/routes
    from app.routes.ai_routes import ai_bp
    from app.routes.vision_routes import vision_bp
    from app.routes.quiz_routes import quiz_bp
    from app.routes.voice_routes import voice_bp
    from app.routes.scientist_routes import science_bp

    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(vision_bp, url_prefix='/api/vision')
    app.register_blueprint(quiz_bp, url_prefix='/api/quiz')
    app.register_blueprint(voice_bp, url_prefix='/api/voice')
    app.register_blueprint(science_bp, url_prefix='/api/science')

    return app
