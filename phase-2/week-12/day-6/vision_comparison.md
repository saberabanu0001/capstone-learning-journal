# Vision System Comparison: Old vs Current

## OLD VISION SYSTEM (Your Original Code)
## vs
## CURRENT VISION SYSTEM (What You're Actually Using Now)

---

## 🎯 **MAJOR DIFFERENCES**

### **1. YOLO Detection - Changed from Always-On to Optional**

**OLD:**
- YOLO detection **always enabled** (no option to disable)
- Detected: person, bottle, cup, cell phone, potted plant
- Used `YoloSpatialDetectionNetwork` with spatial coordinates
- Voice feedback with `subprocess.Popen(['say', phrase])`
- Visual display with bounding boxes
- **Main purpose**: Object detection and announcement

**CURRENT:**
- YOLO detection **optional** via `enable_person_detection=False` parameter
- Only detects **person** (class 0 from COCO)
- Same `YoloSpatialDetectionNetwork` but with depth alignment fix
- **No voice feedback** (removed `say` command)
- **No visual display** (no cv2.imshow or bounding boxes)
- **Main purpose**: Navigation with optional person detection
- Has `detect_person()` method to get person detections programmatically
- Has `get_person_direction()` to determine if person is left/center/right

---

### **2. Camera Pipeline - Improved**

**OLD:**
```python
# Simple pipeline
cam_rgb.setPreviewSize(640, 352)  # Different resolution
stereo.setDepthAlign(dai.CameraBoardSocket.CAM_A)  # Wrong alignment
# No depth alignment fix
```

**CURRENT:**
```python
# Better pipeline
camRgb.setPreviewSize(640, 480)  # Standard resolution
stereo.setDepthAlign(dai.CameraBoardSocket.RGB)  # ✅ FIXED - aligns to RGB
# Tries HIGH_ACCURACY preset, falls back gracefully
# Optional person detection integrated cleanly
```

**Key Improvement**: `setDepthAlign(dai.CameraBoardSocket.RGB)` fixes spatial detection warnings

---

