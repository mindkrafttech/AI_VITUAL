from .vector_store import search_science
import os

def generate_tutor_response(question: str, context: str) -> dict:
    """
    The core logic brain. 
    1. It searches the Vector DB for ground truth scientific data.
    2. It constructs a persona prompt incorporating that scientific truth.
    3. Send this prompt to the LLM (Gemini 2026 SDK).
    """
    from dotenv import load_dotenv
    load_dotenv(override=True)
    google_api_key = os.getenv("GOOGLE_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    google_base_url = os.getenv("GOOGLE_API_BASE_URL")

    print(f"[{context}] Processing Question: {question}")
    print(f"Debug: Google Key Found: {bool(google_api_key)}, OpenAI Key Found: {bool(openai_api_key)}")
    
    # 1. Retrieval (RAG Query)
    retrieved_facts = search_science(question, n_results=1)
    fact_string = "\n".join(retrieved_facts) if retrieved_facts else "No specific scientific data found in our local knowledge vault."
    
    # 2. Persona Prompt Formulation
    system_prompt = f"""
    You are an advanced AI Tutor named "Diamond AI". 
    Your goal is to provide a high-fidelity, comprehensive answer to the user's question about {context}.
    
    GROUND TRUTH SCIENTIFIC FACTS FROM THE VAULT:
    {fact_string}
    
    INSTRUCTIONS:
    1. Provide the direct scientific answer immediately. Do NOT include greetings, intros, or disclaimers about the Knowledge Vault or your source of data.
    2. Base your answer PRIMARILY on any Vault Facts provided above, but seamlessly combine them with your general scientific knowledge for a complete, master-level explanation.
    3. Focus on 'Grading' the concepts—explaining them with total accuracy and high-fidelity details.
    4. Maintain the professional Diamond AI persona without being wordy about your own internal processes.
    """
    
    tutor_answer = ""
    provider_used = "None"
    last_error = "No models attempted"
    all_tried_errors = []

    try:
        if google_api_key:
            # TRY 1: New google-genai library with dynamic model detection
            try:
                from google import genai as genai_new
                client_kwargs = {"api_key": google_api_key}
                if google_base_url:
                    client_kwargs["http_options"] = {"base_url": google_base_url}
                    print(f"[AI-SYNC] Using Proxy Base URL: {google_base_url}")
                
                client = genai_new.Client(**client_kwargs)
                
                # Dynamically find an available model
                available_models = []
                try:
                    all_available = client.models.list()
                    available_models = [m.name for m in all_available if 'generateContent' in m.supported_generation_methods]
                except Exception as e:
                    print(f"[AI-SYNC] Model listing failed: {e}")
                
                # Robust Fallback List (Trying multiple formats)
                fallback_list = [
                    "gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro",
                    "models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-1.0-pro",
                    "gemini-pro"
                ]
                
                # Combine dynamic and fallback, preserving order
                models_to_test = available_models if available_models else fallback_list
                
                for model_name in models_to_test:
                    try:
                        print(f"[AI-SYNC] Attempting: {model_name}")
                        response = client.models.generate_content(model=model_name, contents=f"{system_prompt}\n\nUser Question: {question}")
                        tutor_answer = response.text
                        if tutor_answer:
                            provider_used = f"Google-GenAI ({model_name})"
                            break
                    except Exception as e: 
                        err_msg = f"{model_name}: {str(e)}"
                        all_tried_errors.append(err_msg)
                        print(f"  > {err_msg}")
                        continue
            except ImportError:
                print("[AI-SYNC] Skipping New SDK (Not Installed)")

            # TRY 2: Legacy google-generativeai library (if Try 1 failed)
            if not tutor_answer:
                try:
                    import google.generativeai as genai_legacy
                    genai_legacy.configure(api_key=google_api_key)
                    
                    legacy_models = []
                    try:
                        all_available_legacy = genai_legacy.list_models()
                        legacy_models = [m.name for m in all_available_legacy if 'generateContent' in m.supported_generation_methods]
                    except: pass

                    if not legacy_models:
                         legacy_models = ["models/gemini-1.5-flash", "models/gemini-pro", "models/gemini-1.0-pro"]

                    for model_name in legacy_models:
                        try:
                            print(f"[AI-SYNC] Dynamic Legacy Attempt: {model_name}")
                            model = genai_legacy.GenerativeModel(model_name)
                            response = model.generate_content(f"{system_prompt}\n\nUser Question: {question}")
                            tutor_answer = response.text
                            if tutor_answer:
                                provider_used = f"Google-Legacy ({model_name})"
                                break
                        except Exception as e: 
                            err_msg = f"Legacy-{model_name}: {str(e)}"
                            all_tried_errors.append(err_msg)
                            print(f"  > {err_msg}")
                            continue
                except ImportError:
                    print("[AI-SYNC] Skipping Legacy SDK (Not Installed)")

            if not tutor_answer:
                # Group errors to show the most relevant ones
                found_403 = any("403" in err for err in all_tried_errors)
                found_404 = any("404" in err for err in all_tried_errors)
                
                if found_403:
                    tutor_answer = "Diamond AI - Sync Error: Permission Denied (403). Your API Key might not have the 'Generative Language API' enabled in Google Cloud Console."
                elif found_404:
                    tutor_answer = "Diamond AI - Sync Error: Model Not Found (404). The models are not accessible with this key. Please ensure you are using a key from Google AI Studio (Makersuite)."
                else:
                    tutor_answer = f"Diamond AI - Sync Error: All model attempts failed. Last error: {all_tried_errors[-1] if all_tried_errors else 'No models found'}"

        elif openai_api_key:
            # Same OpenAI logic if ONLY OpenAI key is provided
            from openai import OpenAI
            client = OpenAI(api_key=openai_api_key)
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": question}]
            )
            tutor_answer = completion.choices[0].message.content
            provider_used = "OpenAI"
        else:
            tutor_answer = f"No API Key found. I retrieved this from my local vault: '{fact_string}'"
            provider_used = "Local Vault Only"
        
        # --- NEW: Generate a concise summary for the 'Quick Glance' UI ---
        tutor_summary = ""
        if tutor_answer and not tutor_answer.startswith("Diamond AI - Sync Error"):
            if google_api_key:
                try:
                    # Re-use the summarization prompt logic
                    summary_prompt = f"Summarize this scientific explanation into 3-5 concise, high-fidelity bullet points. Zero fluff:\n\n{tutor_answer}"
                    from google import genai
                    client = genai.Client(api_key=google_api_key)
                    sum_resp = client.models.generate_content(model="gemini-1.5-flash", contents=summary_prompt)
                    tutor_summary = sum_resp.text
                except Exception as sum_err:
                    print(f"[AI-SUMMARY] GenAI Summary Failed: {sum_err}")
                    # Fallback to logic below
                    pass
            
            if not tutor_summary:
                # Fallback: Just take the first few lines
                lines = [l.strip() for l in tutor_answer.split('\n') if l.strip()]
                tutor_summary = "\n".join(lines[:3]) + "..." if len(lines) > 3 else tutor_answer

    except Exception as e:
        error_msg = str(e)
        print(f"--- AI ENGINE ERROR ---\n{error_msg}")
        return {
            "status": "error",
            "student_query": question,
            "tutor_response": f"Diamond AI - Critical Error: {error_msg}",
            "provider": "Sync Error"
        }

    return {
        "status": "success",
        "question": question,
        "vault_sources_used": len(retrieved_facts),
        "tutor_response": tutor_answer,
        "tutor_summary": tutor_summary,
        "provider": provider_used
    }

def generate_research_summary(topic: str) -> dict:
    """
    Specifically designed for 'Quick Research' – high-fidelity, concise bullet points.
    Uses RAG to ensure the summary is based on the Knowledge Vault's scientific truth.
    """
    from dotenv import load_dotenv
    load_dotenv(override=True)
    google_api_key = os.getenv("GOOGLE_API_KEY")

    # 1. Retrieval
    retrieved_facts = search_science(topic, n_results=2)
    fact_string = "\n".join(retrieved_facts) if retrieved_facts else "No specific vault data."

    # 2. Refined Summary Prompt
    summary_prompt = f"""
    You are Diamond AI. Provide a MASTER-LEVEL scientific research summary for the topic: {topic}.
    
    VAULT DATA:
    {fact_string}
    
    STRICT INSTRUCTIONS:
    1. Output exactly 5-7 concise, high-impact bullet points.
    2. Zero greetings, zero intros, zero fluff. 
    3. Use technical, accurate terminology (Grading the concept).
    4. Focus on core mechanics, definitions, and significance.
    5. Format with '*' as bullet markers.
    """

    summary_text = ""
    provider = "None"

    try:
        # 1. Try New SDK (Fastest)
        from google import genai
        client = genai.Client(api_key=google_api_key)
        
        # Robust candidate list for the new SDK
        for model_candidate in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp", "gemini-pro"]:
            try:
                response = client.models.generate_content(
                    model=model_candidate,
                    contents=summary_prompt
                )
                summary_text = response.text
                if summary_text:
                    provider = f"Google Gemini (Flash - {model_candidate})"
                    break
            except Exception as e:
                print(f"[AI-RESEARCH] Candidate {model_candidate} failed: {e}")
                continue

    except Exception as e:
        print(f"[AI-RESEARCH] New SDK setup failed: {e}. Attempting Legacy Fallback...")

    if not summary_text:
        try:
            # 2. Try Legacy SDK (Robust Fallback)
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=google_api_key)
            
            # Legacy candidates
            for model_candidate in ["models/gemini-1.5-flash", "models/gemini-pro", "gemini-pro", "models/gemini-1.0-pro"]:
                try:
                    model = genai_legacy.GenerativeModel(model_candidate)
                    response = model.generate_content(summary_prompt)
                    summary_text = response.text
                    if summary_text:
                        provider = f"Google Gemini (Legacy - {model_candidate})"
                        break
                except Exception as e:
                    print(f"[AI-RESEARCH] Legacy Candidate {model_candidate} failed: {e}")
                    continue
        except Exception as legacy_err:
            print(f"[AI-RESEARCH] Legacy SDK setup failed: {legacy_err}")

    if not summary_text:
        # 3. Final Fallback (Text-based from Vault)
        summary_text = f"* Local Vault Insight: {fact_string[:300]}..."
        provider = "Local Vault (AI Synthesis Failed)"

    return {
        "status": "success",
        "topic": topic,
        "summary": summary_text,
        "provider": provider
    }
