import base64
import os
from google import genai
from flask import Blueprint, request, jsonify, current_app
from app.ai_engine.tutor_logic import generate_tutor_response

vision_bp = Blueprint('vision', __name__)

@vision_bp.route('/analyze', methods=['POST'])
def analyze_image():
    """
    Endpoint for processing Multimodal / OCR image inputs from the frontend.
    Uses Gemini 1.5 Flash to extract text/formulas and explain steps.
    """
    data = request.json
    if not data or 'image_data' not in data:
        return jsonify({"error": "Missing image_data parameter"}), 400
        
    image_b64 = data.get('image_data')
    student_context = data.get('context', 'general')
    
    print(f"[{student_context}] Analyzing incoming Multimodal Image data with Gemini...")
    
    google_key = os.getenv("GOOGLE_API_KEY")
    google_base_url = os.getenv("GOOGLE_API_BASE_URL")
    
    if not google_key:
        return jsonify({"status": "error", "message": "Google API key not configured for vision."}), 500

    try:
        client_kwargs = {"api_key": google_key}
        if google_base_url:
            client_kwargs["http_options"] = {"base_url": google_base_url}
        
        client = genai.Client(**client_kwargs)
        
        # 1. Dynamically find a suitable multimodal model
        try:
            # Look for models that support vision (multimodal)
            # Typically these are 'gemini-1.5-flash' or 'gemini-1.5-pro'
            all_models = client.models.list()
            vision_models = [m.name for m in all_models if 'generateContent' in m.supported_generation_methods]
            
            # Prioritize flash for speed in vision tasks
            if any("gemini-1.5-flash" in m for m in vision_models):
                model_name = next(m for m in vision_models if "gemini-1.5-flash" in m)
            elif vision_models:
                model_name = vision_models[0]
            else:
                model_name = "gemini-1.5-flash" # Absolute fallback
        except Exception as e:
            print(f"[VISION-SYNC] Model listing failed: {e}")
            model_name = "gemini-1.5-flash"

        clean_model_name = model_name.replace("models/", "")
        print(f"[VISION-SYNC] Selected Multimodal Model: {clean_model_name}")

        # 2. Prepare Multimodal Prompt
        prompt = """
        Examine this image carefully. 
        1. Extract any mathematical equations, scientific text, or diagrams you see.
        2. Format the output as a clear 'EXTRACTION' string.
        3. Provide exactly 3 or 4 logical 'STEPS' to solve or explain what is in the image.
        Format example:
        EXTRACTION: [The text or formula]
        STEP 1: [Short description]
        STEP 2: [Short description]
        """

        # 3. Call Gemini for Multimodal Vision
        response = client.models.generate_content(
            model=clean_model_name,
            contents=[
                prompt,
                {'mime_type': 'image/png', 'data': image_b64}
            ]
        )
        
        full_text = response.text
        
        # 3. Parse Gemini Response
        lines = full_text.split('\n')
        extracted_text = "Analysis complete"
        steps = []

        for line in lines:
            if "EXTRACTION:" in line.upper():
                extracted_text = line.split(":", 1)[1].strip()
            elif "STEP" in line.upper() and ":" in line:
                steps.append(line.split(":", 1)[1].strip())

        # 4. Fallback to RAG for deep tutor explanation
        tutor_data = generate_tutor_response(f"Explain this in detail: {extracted_text}", student_context)
        tutor_answer = tutor_data.get('tutor_response', "Could not generate analysis.")
        provider = tutor_data.get('provider', 'Unknown')
        
        # 5. Finalize Front-end Response
        return jsonify({
            "answer": tutor_answer,
            "provider": provider,
            "vision_extraction": extracted_text,
            "steps": steps if steps else ["Analysis successful", "Vault lookup performed"]
        }), 200

    except Exception as e:
        print(f"[VISION ERROR] Gemini Vision failed: {e}")
        return jsonify({"error": "Failed to analyze image with Gemini Vision", "details": str(e)}), 500
