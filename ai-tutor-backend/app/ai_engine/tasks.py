from celery_worker import celery_app
import time

@celery_app.task(bind=True)
def generate_complex_animation_data(self, topic):
    """
    Mock asynchronous task to generate heavy data (like 3D animations or deep analysis)
    in the background without freezing the UI.
    """
    print(f"[Async Task] Starting generation of complex animation for {topic}...")
    
    # Simulate heavy processing (e.g., calling an external rendering API or LLM)
    time.sleep(5) 
    
    print(f"[Async Task] Completed generation for {topic}")
    return {"topic": topic, "animation_url": f"https://s3.aws.com/animations/{topic}_render.mp4", "status": "completed"}
