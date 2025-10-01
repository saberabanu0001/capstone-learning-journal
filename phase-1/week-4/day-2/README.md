# 📖 Week-4 Day-2 — VisionSystem Foundation
## 🎯 Goal

Build the VisionSystem class (v1.0) → a reusable module to get live RGB frames from the OAK-D Lite camera.

This marks the foundation of our computer vision system.

## 🧩 What I Did

 - Created a new module: modules/vision.py.

 - Defined a VisionSystem class.

- Inside, built a DepthAI pipeline:

- Configured the OAK-D Lite’s RGB camera.

- Linked it to an output queue.

- Added a function get_latest_frame() → returns the current RGB frame.

- Wrote test_vision.py:

- Imported VisionSystem.

- Continuously grabbed frames using get_latest_frame().

- Displayed them in an OpenCV window.

## 📂 Files Created / Updated

modules/vision.py → VisionSystem class with RGB pipeline.

test_vision.py → test script to view live camera feed.

### ▶️ How to Run

- Activate virtual environment:

source depthai-env/bin/activate


- Run test:

python3 test_vision.py


- Press q to quit.

### 🖥️ Output (Simulation Mode)

OpenCV window:

Shows a blue screen (fake image in simulation).

With real hardware, this will be the live RGB camera feed.

Terminal (when frame is available):

[VisionSystem] Capturing RGB frame...

## ✅ Learning Outcome

- Understood how to create a DepthAI pipeline in Python.

- Learned how to capture and display RGB frames with DepthAI + OpenCV.

- Built the first version of Vision Module (v1.0) → foundation for all future vision work.

✨ Next step (Day-3): Add depth support (get_center_depth()) to measure distances.