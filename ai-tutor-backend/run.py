import threading
import sys
import traceback
import os

print("\n[DIAGNOSTIC] Initializing Diamond AI Modules...")
print("[DIAGNOSTIC] Python Version:", sys.version)

try:
    print("[DIAGNOSTIC] Loading App Logic...")
    from app import create_app
    print("[DIAGNOSTIC] Connecting to Knowledge Scrapers...")
    from scraper import start_hourly_update
    
    print("[DIAGNOSTIC] Initializing AI Engine (First-time download may take 2-3 mins)...")
    # This is where it downloads the large 'all-MiniLM-L6-v2' model
    app = create_app()
    print("[DIAGNOSTIC] App Created Successfully.")
except Exception as e:
    print("\n" + "!"*50)
    print("   CRITICAL ERROR DURING INITIALIZATION")
    print("!"*50)
    traceback.print_exc()
    print("\n[HINT] This often happens if the initial AI model download is blocked by a firewall.")
    print("[HINT] Ensure you have a stable internet connection.")
    input("\nPress ENTER to close this diagnostic window...")
    sys.exit(1)

if __name__ == "__main__":
    try:
        # Start the scraper loop in a background thread
        scraper_thread = threading.Thread(target=start_hourly_update, args=(app,), daemon=True)
        scraper_thread.start()

        print("\n" + "="*50)
        print("   DIAMOND AI SERVER IS LIVE")
        print("   URL: http://127.0.0.1:5000")
        print("="*50 + "\n")
        
        # Switched to 127.0.0.1 for maximum local reliability
        app.run(host="127.0.0.1", port=5000, debug=False)
    except Exception as e:
        print(f"\n[SERVER FATAL ERROR] {e}")
        traceback.print_exc()
        input("\nPress any key to close this diagnostic window...")
