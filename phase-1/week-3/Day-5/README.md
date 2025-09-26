# 📅 Day-5: Testing Environment & First Custom Script  

## 🎯 Goal  
* Test the OAK-D Lite setup in VS Code.  
* Confirm DepthAI API is working.  
* Build the first **custom script (`test_camera.py`)**.  

---

## 🔗 What I Did  

### 1. Environment Setup (MacBook)  
* Created a virtual environment:  
  ```bash
  python3 -m venv depthai-env
  source depthai-env/bin/activate
* Installed DepthAI:
- pip install depthai
* Cloned the official DepthAI repository:
- git clone https://github.com/luxonis/depthai-python.git
### 2. Running Example (rgb_preview.py)
Tried to run rgb_preview.py from examples/ColorCamera.

Since hardware is not yet available, script showed:
- RuntimeError: No available devices
✅ This is expected — it means the software environment is ready, just waiting for the OAK-D Lite.

### 3. My Own Script: test_camera.py
Instead of only running examples, I wrote a simple custom script.

* What it does:

- Creates a pipeline.

- Turns on the RGB camera.

- Sends frames to the host computer.

- Displays live video feed (once camera is connected).

## 🔍 Why This Matters
- Proves I understand DepthAI pipelines, not just copy–pasting examples.

- Gives us a debugging tool: later, if anything fails, I can run test_camera.py to confirm if the camera works.

- Acts as the foundation for Week-4’s official vision.py module (with reusable functions).

📊 Data Flow (Day-5)

### [OAK-D Lite RGB Camera] → [DepthAI Pipeline] → [Host Display Window]
When hardware is connected, this will show the first live image feed.

### ✅ Summary
Environment fully set up (DepthAI installed, repo cloned).

Explored official examples (rgb_preview.py, stereo_depth.py, etc.).

Built my own custom script (test_camera.py).

Currently blocked only by missing hardware — once it arrives, live video will work immediately.