📅 Week 3: First Image & Pipeline Basics
🔗 Connection to Previous Work
Week 2: The robot could see raw pixels using the camera.
Week 3: The robot now learns to capture and display those pixels via a DepthAI pipeline, creating the software foundation for all future vision tasks.

📋 test_camera.py
This script proves that the software and hardware are correctly communicating. It's the robot's first live view of the world.

Pipeline Comparison:

Week 2: [Camera] -> [Raw Pixels]

Week 3: [Camera (ColorCamera)] -> [XLinkOut] -> [Display with OpenCV]

🛠️ What the Code Does
This foundational script does the following:

Creates a DepthAI pipeline.

Captures frames from the ColorCamera node.

Sends frames to the host computer using the XLinkOut node.

Displays a live video feed using OpenCV.

Includes print statements for debugging, allowing us to confirm the code works even without the camera plugged in.

🚀 How to Run
Follow these steps to test the script yourself:

Activate your virtual environment:

Bash

source depthai-env/bin/activate
Install dependencies:

Bash

pip install depthai opencv-python
Run the script:

Bash

python test_camera.py
🔎 Expected Output
Without OAK-D Lite plugged in:

Plaintext

🚀 Starting test_camera.py...
✅ Pipeline created.
📷 Camera node configured and linked.
❌ Could not connect to device. Maybe the OAK-D Lite is not plugged in?
Error details: ...
With OAK-D Lite connected:
A window opens showing a live video feed. Press q to exit.

🎯 Deliverable Goals
Proves the ability to create and run a DepthAI pipeline from scratch.

Establishes the foundation for Week 4, where the pipeline will be expanded into a more structured vision.py module.

Ensures frames are being captured and are ready for future computer vision tasks.