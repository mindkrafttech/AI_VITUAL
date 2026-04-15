import os
from flask import Blueprint, request, jsonify
from app.ai_engine.tutor_logic import generate_tutor_response

voice_bp = Blueprint('voice', __name__)

@voice_bp.route('/transcribe', methods=['POST'])
def handle_voice_query():
    """
    Endpoint for Voice-to-Knowledge (Whisper AI) processing.
    Expects a multipart form POST with an 'audio' file.
    """
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
        
    audio_file = request.files['audio']
    
    print("[Whisper AI] Received audio blob. Transcribing to text...")
    
    # 1. Processing the Audio (Mocked Whisper AI Connection)
    # In production, this would save the blob to temp storage and pass it to openai.audio.transcriptions.create(model="whisper-1")
    
    # Simulated Whisper AI Transcription
    simulated_transcript = "Can you clearly explain Newton's second law?"
    print(f"[Whisper AI] Transcribed text: '{simulated_transcript}'")
    
    # 2. RAG Pipeline
    # Pass the transcribed text natively into the Knowledge Vault logic engine
    response_data = generate_tutor_response(simulated_transcript, "physics")
    
    # 3. Enhance response with Voice TTS markers
    response_data['transcript'] = simulated_transcript
    
    # Simulate a generated Text-To-Speech audio URL
    response_data['audio_url'] = "https://s3.aws.com/science-assets/generated_tts/newton_explanation.mp3"
    
    return jsonify(response_data), 200
