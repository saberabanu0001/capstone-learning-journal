from modules.vision import VisionSystem

vision = VisionSystem(simulate=True)
detections = vision.get_detections_with_depth()
for d in detections:
    print(f"[TEST] {d['label']} ({d['confidence']*100:.1f}%) "
          f"at X={d['x']}mm, Y={d['y']}mm, Z={d['z']}mm")
 