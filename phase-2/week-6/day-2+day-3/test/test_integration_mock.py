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

# --- Start Simulation ---
vision = VisionSystem(simulate=True)
print("🔹 Starting Vision–Audio Integration Mock Test...\n")

for i in range(5):
    detections = vision.get_detections_with_depth()
    if not detections:
        print(f"[Cycle {i+1}] No detections.")
    else:
        for d in detections:
            label = d["label"]
            distance = d["coords_mm"][2] / 1000.0  # convert mm → meters
            print(f"[Vision] Detected {label} at {distance:.2f}m")
            print(simulate_audio_response(label, distance))
    print("----")
    time.sleep(1)

print("\n✅ Integration Mock Test Complete.")
