# test/test_integration_mock.py

from modules.vision import VisionSystem
import time

# --- Simulated integration test between Vision and Audio ---
def simulate_audio_response(label, distance):
    """Mock audio system response"""
    if label == "person":
        return f"[Audio Mock] 🗣️ 'Person detected at {distance:.1f} meters.'"
    elif label == "car":
        return f"[Audio Mock] 🚗 'Car ahead, approximately {distance:.1f} meters away.'"
    elif label == "dog":
        return f"[Audio Mock] 🐶 'Dog detected at {distance:.1f} meters.'"
    else:
        return f"[Audio Mock] 🔍 'Detected a {label} at {distance:.1f} meters.'"


