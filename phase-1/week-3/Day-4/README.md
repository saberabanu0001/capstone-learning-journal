# 📅 Day-4: Spatial Object Detection (What + Where)

## 🔗 Recap
- **Day-2**: The robot can see **RGB frames** and **depth maps**.  
- **Day-3**: The robot can use a **Neural Network** to detect objects (like “person”, “dog”, “car”).  
- **Day-4**: Combine them → not only *“what object is this?”* but also *“how far away is it?”*  

---

## ⚡ Why This Matters
For the project:
- **Week-6 = Person Detection** ✅  
- But the robot doesn’t just need to know *“a person exists.”*  
- It must also know *“where they are”* (distance + position).  

This allows the robot to:
- Avoid obstacles.  
- Follow people.  
- Interact with the environment intelligently.  

---

## 🤖 What `spatial_mobilenet.py` Does
Think of it like a recipe your OAK-D Lite camera follows:

### 1. Load a brain (the AI model)
- Loads a **MobileNetSSD model**.  
- Pre-trained to recognize ~20 everyday objects (person, car, dog, chair, etc.).  

### 2. Turn on the cameras
- **RGB camera**: captures color images for object detection.  
- **Two mono cameras**: capture left + right grayscale views for depth.  
- **StereoDepth node**: calculates how far things are (like human eyes).  

### 3. Run detection with depth awareness
- RGB frames go to the **Myriad X chip** running MobileNetSSD.  
- StereoDepth provides a **depth map (in millimeters)**.  
- The **Spatial Detection Network** fuses both → each detection has a label + 3D coordinates.  

### 4. Send results back to computer/Jetson
- The program outputs:  
  - Live RGB video feed.  
  - List of detections (object name, confidence, bounding box).  
  - **Spatial coordinates (X, Y, Z in mm)** for each object.  

### 5. Draw boxes + depth info on video
On your screen you see two windows:  

- **Preview (RGB feed)**:  
  - Rectangles around detected objects.  
  - Labels (e.g., “person”).  
  - Confidence (e.g., 91%).  
  - Coordinates: X, Y, Z in millimeters.  

- **Depth (colorized map)**:  
  - Shows distances as colors (red = near, blue = far).  
  - Bounding boxes overlaid to match detections.  

### 6. Repeat continuously
- Runs many times per second.  
- Gives **real-time 3D object detection**, e.g.:  
---

# Enhanced-----
## 📌 Why you still see YOLO detections without a camera

**Right now, in our VisionSystem (modules/vision.py), we set:**

**vision = VisionSystem(simulate=True)**


#### That simulate=True flag tells the code:
👉 “Pretend we have a camera, and generate fake detections + fake depth values.”

#### This was done so that:

- You can develop and test the pipeline even without hardware.

- You can show progress to professor (detections, depth, etc.) before the OAK-D actually arrives.

### 📊 Where the values come from

- label: random choices like "person", "car", "dog".

- confidence: random % values like 62.0%, 90.0% …

- coords_mm: simulated 3D coordinates (X, Y, Z in millimeters).

**So right now → it’s just mock data (like a fake sensor).**
**Once the OAK-D camera arrives, you’ll change:**

- vision = VisionSystem(simulate=False)


## Then:

- The detections will come from the real YOLO model running on the OAK-D.

- The depth values will be measured by stereo depth sensors inside the camera.