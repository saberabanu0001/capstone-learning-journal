# 📖 Week-4 Day-3 — Depth Support
## 🎯 Goal

Extend the VisionSystem to not only capture RGB frames but also measure depth (distance) using the OAK-D Lite’s stereo cameras.

## 🧩 What I Did

 - Updated modules/vision.py:

 - Added stereo camera setup (left + right mono cams).

 - Linked them to a StereoDepth node.

 - Added get_center_depth() → returns distance (in mm) at the image center.

 - Added simulation mode: if no OAK-D Lite is connected, generate random depth values (0.5–3m).

 - Updated test_vision.py:

 - Displays RGB frames (blue screen in simulation).

 - Prints center depth values in meters.

 - Runs until you press q.

## 📂 Files Created / Updated

 - modules/vision.py → VisionSystem class extended with depth support

 - test_vision.py → test script for RGB + depth

## ▶️ How to Run

 - Activate virtual environment:

 - source depthai-env/bin/activate


Run test:

 - python3 test_vision.py


 - Press q to quit.

## 🖥️ Output (Simulation Mode)

 - OpenCV window → Blue image (simulated RGB feed)

- Terminal → prints random distances like:

Center depth: 1.57 meters
Center depth: 2.61 meters
Center depth: 0.95 meters


With real hardware, these numbers will be actual distances from the camera.

## ✅ Learning Outcome

- Learned how stereo vision works with OAK-D Lite.

- Built a function to retrieve depth information in real-time.

- Confirmed simulation works → ready to test on real hardware.

✨ Next step (Day-4): Combine object detection + depth so the robot knows what object is detected and how far away it is.