# Big Picture (OAK-D Lite Overview)

## Goal
Understand what the OAK-D Lite camera is and why it’s special.

## Key Learnings
- **RGB Camera**  
  Captures high-resolution color images (like a normal webcam).  
  Useful for object detection, face recognition, and seeing textures.

- **Stereo Depth Cameras**  
  Two small monochrome sensors placed apart (like human eyes).  
  They calculate distance (depth map) so the robot knows *how far* objects are.  
  Ideal depth range: ~0.8m – 12m.

- **Myriad X (RVC2 VPU)**  
  Built-in AI chip inside the camera.  
  Runs neural networks directly on the device (person detection, object tracking).  
  Reduces load on the Jetson Orin NX.

## Diagram – Data Flow
[OAK-D Lite: RGB + Stereo + Myriad X] → [Jetson Orin NX] → [ROS2] → [Robot Actions]

## One Useful Spec
- RGB camera: 12MP, auto-focus, ~81° FOV.  
- Stereo cameras: 86° FOV, ~2% depth error up to 4m.  
- Myriad X: 1.4 TOPS for AI tasks.

---
# DepthAI Basics

## Goal
Understand the DepthAI software library and the concept of pipelines.

## Key Learnings
- **Pipeline**  
  A chain of nodes where data flows: camera → processing → output.  
  Like a conveyor belt for vision tasks.

- **RGB Preview**  
  Example pipeline that streams live color video frames.  
  Built with a `ColorCamera` node linked to `XLinkOut`.

- **Stereo Depth**  
  Example pipeline using two mono cameras to create a depth map (distance image).  
  Output can tell how far objects are in millimeters.

- **Object Detection**  
  Runs a pre-trained AI model on the Myriad X chip.  
  Instead of sending full video to Jetson, it can directly output “person detected.”

## Example Pipeline Diagram

[Camera Node] → [Neural Network / Depth Node] → [XLinkOut] → [Host PC (OpenCV)]


## Code Snippet (from rgb_preview.py)
```python
pipeline = dai.Pipeline()
cam = pipeline.create(dai.node.ColorCamera)
xout = pipeline.create(dai.node.XLinkOut)
cam.preview.link(xout.input)
