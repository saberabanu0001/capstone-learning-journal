## 🧠 Vision Module – AI Rover Project

 - Owner: Sabera Banu
- Phase: Vision System (Weeks 4–5)
- Platform: OAK-D / DepthAI / Jetson

## 📖 Overview

This module handles the visual perception of the AI Rover.
It captures frames from the OAK-D camera, performs YOLO-based object detection, and estimates depth for navigation.
It supports both:

### ✅ Real Hardware Mode – OAK-D camera

#### 🧩 Simulation Mode – Webcam or dummy data

#### ⚙️ Implemented Features
## Week 4 – Vision Foundation

Initialized DepthAI camera pipeline (RGB + depth).

### Implemented:

- get_latest_frame() – Capture RGB frame

- get_center_depth() – Get central depth distance

- Added simulation mode (dummy or webcam input).

## Week 5 – YOLO Integration

- Integrated YOLO Spatial Detection Network.

- Added get_detections_with_depth() for object + depth output.

- Created test scripts for camera, depth, and detection validation.

### 🧩 VisionSystem Class
#### class VisionSystem:
    - def get_latest_frame()
    - def get_center_depth()
    - def get_detections_with_depth()


#### Example simulated output:

- [YOLO] person (91%) at X=70mm, Y=63mm, Z=2184mm
- Center depth: 1.57 m

### 🧪 Testing
**Script	Purpose**
- test_camera.py	Tests frame capture
- test_depth.py	Tests depth reading
- test_yolo.py	Tests object detection
- test_integration.py	Combined system test

**Run test:**

- python3 -m test.test_camera

## 📅 Progress Summary
Week	Task	Status
Week 4	Vision system setup	✅
Week 5	YOLO detection integration	✅
Week 6	Hardware testing (Jetson + OAK-D)	🔄 Upcoming
## 🔮 Next Steps

- Test on real hardware (OAK-D).

- Fine-tune YOLO for specific objects.

- Begin integration with motor and audio modules.