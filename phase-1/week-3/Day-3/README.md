# 📅 Day-3: Object Detection with MobileNetSSD

## 🔗 Connection Between Day-2 & Day-3
- **Day-2**: Robot now can *see* raw pixels and measure distances.
- **Day-3**: Robot learns to *understand* what it sees.

Examples:
- “That’s a person at 2.5m”
- “That’s a chair, don’t crash into it”

This understanding comes from **Object Detection models** like MobileNetSSD or YOLO.

### Pipeline Comparison
- **Day-2**: [Camera] → [Output to Jetson]
- **Day-3**: [Camera] → [Neural Network (Myriad X)] → [Detections to Jetson]

---

## 🚀 Why This Matters for the Final Robot
- Project proposal (Week-6) = **Person Detection**.  
- Day-3 prepares exactly for this step.  
- By understanding MobileNetSSD now, you’ll later be able to:
  - Swap in a dedicated *person detection* model.
  - Combine detection with depth → know how far a person is.
  - Integrate results into Jetson/ROS2 for robot decisions.

---

## 🌍 Big Picture Roadmap
- **Day-1** = Camera hardware basics (RGB, Depth, Myriad X)  
- **Day-2** = Building pipelines (raw RGB, depth maps)  
- **Day-3** = Adding intelligence (object detection with NN)  

---

## 🧠 MobileNetSSD
- **MobileNet** = lightweight deep neural network, efficient for mobile/embedded devices.  
- **SSD (Single Shot Detector)** = predicts classes + bounding boxes in a single pass (fast).  
- **Together (MobileNetSSD)** =  
  - Pre-trained to recognize ~20 everyday classes (person, car, dog, chair, etc.).  
  - Balanced between speed and accuracy.  
  - Well-suited for OAK-D Lite’s **Myriad X** chip.

---

## ⚡ YOLO (Alternative)
- **YOLO = You Only Look Once**  
- Very popular, also designed for *real-time detection*.  
- Detects all objects in one pass (very fast).  
- Can be used instead of MobileNetSSD depending on project needs.  
- YOLO examples are in `examples/Yolo/` in the repo.

---

## 🤖 What `rgb_mobilenet.py` Does
Think of it like a recipe your OAK-D follows:

1. **Load a brain (AI model)**  
   - Loads the MobileNetSSD model (pre-trained on 20 objects).  

2. **Turn on the camera**  
   - RGB camera starts capturing frames.  
   - Each frame resized to 300×300 (model input size).  

3. **Run detection on the camera itself**  
   - Frames sent into Myriad X chip.  
   - Model checks if objects are present.  

4. **Send results back to Jetson/PC**  
   - Sends both: live image + list of detections (object, confidence, bounding box).  

5. **Draw boxes on the video**  
   - Bounding boxes drawn with labels + confidence score (e.g., “person 87%”).  

6. **Repeat continuously**  
   - Runs in real-time, showing live detections.  

---

✅ **Takeaway**:  
Day-3 transforms the robot from just *seeing* to actually *understanding* the world through object detection.  
