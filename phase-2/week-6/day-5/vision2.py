import depthai as dai
import cv2
import numpy as np
import time

# ─────────────────────────────────────────────
# YOLO labels you care about (COCO equivalents)
# ─────────────────────────────────────────────
TARGET_LABELS = [
    "person",          # person
    "cell phone",      # mobile
    "bottle",          # bottle
    "cup",             # cup
    "pen",             # pen-like (YOLO doesn’t have “pen”; might not detect)
    "potted plant",    # plant
    "sports ball",     # use for “doll” approximation
]

# ─────────────────────────────────────────────
# Load COCO labels (same order as training)
# ─────────────────────────────────────────────
LABEL_MAP = [
    "person","bicycle","car","motorbike","aeroplane","bus","train","truck","boat",
    "traffic light","fire hydrant","stop sign","parking meter","bench","bird","cat",
    "dog","horse","sheep","cow","elephant","bear","zebra","giraffe","backpack",
    "umbrella","handbag","tie","suitcase","frisbee","skis","snowboard","sports ball",
    "kite","baseball bat","baseball glove","skateboard","surfboard","tennis racket",
    "bottle","wine glass","cup","fork","knife","spoon","bowl","banana","apple",
    "sandwich","orange","broccoli","carrot","hot dog","pizza","donut","cake","chair",
    "sofa","potted plant","bed","dining table","toilet","tvmonitor","laptop","mouse",
    "remote","keyboard","cell phone","microwave","oven","toaster","sink","refrigerator",
    "book","clock","vase","scissors","teddy bear","hair drier","toothbrush"
]

# ─────────────────────────────────────────────
# Vision system class
# ─────────────────────────────────────────────
class VisionSystem:
    def __init__(self):
        print("🎥 Initializing OAK-D Lite Vision System…")
        self.pipeline = self.create_pipeline()
        self._z_ema = {}  # for smoothing depth
        self.device = dai.Device(self.pipeline)
        self.q_rgb = self.device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
        self.q_det = self.device.getOutputQueue(name="detections", maxSize=4, blocking=False)

    # ─────────────────────────
    # Create DepthAI pipeline
    # ─────────────────────────
    def create_pipeline(self):
        print("🔧 Building DepthAI pipeline…")
        pipeline = dai.Pipeline()

        # Color camera
        cam_rgb = pipeline.createColorCamera()
        cam_rgb.setPreviewSize(640, 352)              # must match your blob
        cam_rgb.setPreviewKeepAspectRatio(False)      # critical for alignment
        cam_rgb.setInterleaved(False)
        cam_rgb.setFps(30)

        # Mono cameras
        monoL = pipeline.createMonoCamera()
        monoR = pipeline.createMonoCamera()
        monoL.setBoardSocket(dai.CameraBoardSocket.LEFT)
        monoR.setBoardSocket(dai.CameraBoardSocket.RIGHT)
        monoL.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)
        monoR.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)

        # Stereo depth
        stereo = pipeline.createStereoDepth()
        stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
        stereo.setLeftRightCheck(True)
        stereo.setSubpixel(True)
        stereo.setDepthAlign(dai.CameraBoardSocket.RGB)
        stereo.setMedianFilter(dai.MedianFilter.KERNEL_5x5)
        stereo.setConfidenceThreshold(200)
        monoL.out.link(stereo.left)
        monoR.out.link(stereo.right)

        # Spatial Detection Network
        detection_nn = pipeline.createYoloSpatialDetectionNetwork()
        detection_nn.setBlobPath("models/yolov8n_coco_640x352.blob")  # blob path
        detection_nn.setConfidenceThreshold(0.4)
        detection_nn.setNumClasses(80)
        detection_nn.setCoordinateSize(4)
        detection_nn.setIouThreshold(0.5)
        detection_nn.setBoundingBoxScaleFactor(0.5)
        detection_nn.setDepthLowerThreshold(100)    # 0.1 m
        detection_nn.setDepthUpperThreshold(4000)   # 4 m
        detection_nn.input.setBlocking(False)

        cam_rgb.preview.link(detection_nn.input)
        stereo.depth.link(detection_nn.inputDepth)

        # Output
        xout_rgb = pipeline.createXLinkOut()
        xout_rgb.setStreamName("rgb")
        detection_nn.passthrough.link(xout_rgb.input)

        xout_nn = pipeline.createXLinkOut()
        xout_nn.setStreamName("detections")
        detection_nn.out.link(xout_nn.input)

        return pipeline

    # ─────────────────────────
    # Main processing loop
    # ─────────────────────────
    def run(self):
        frame_count = 0
        print("✅ Starting detection. Press Q to quit.")

        while True:
            in_rgb = self.q_rgb.tryGet()
            in_det = self.q_det.tryGet()
            if not in_rgb:
                continue

            frame = in_rgb.getCvFrame()
            if in_det:
                detections = in_det.detections
                for det in detections:
                    label = LABEL_MAP[det.label]
                    if label not in TARGET_LABELS:
                        continue

                    # Bounding box
                    x1 = int(det.xmin * frame.shape[1])
                    y1 = int(det.ymin * frame.shape[0])
                    x2 = int(det.xmax * frame.shape[1])
                    y2 = int(det.ymax * frame.shape[0])

                    # Depth → meters
                    depth_m = det.spatialCoordinates.z / 1000.0
                    conf = det.confidence * 100

                    # EMA smoothing
                    key = det.label
                    prev = self._z_ema.get(key, depth_m)
                    depth_m = 0.3 * depth_m + 0.7 * prev
                    self._z_ema[key] = depth_m

                    # Draw + print
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        f"{label} {conf:.1f}% ({depth_m:.2f} m)",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 255),
                        2,
                    )
                    print(f"[Vision] {label} ({conf:.1f}%) – {depth_m:.2f} m away")

            cv2.imshow("Vision Detection", frame)
            if cv2.waitKey(1) == ord("q"):
                break

        cv2.destroyAllWindows()
        print("🛑 Stopped. ✅ Vision module complete.")

# ─────────────────────────
# Run directly
# ─────────────────────────
if __name__ == "__main__":
    vision = VisionSystem()
    vision.run()
