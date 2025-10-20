import depthai as dai
import cv2
import numpy as np
import time

# ─────────────────────────────
# Target labels for detection
# ─────────────────────────────
TARGET_LABELS = ["person", "cell phone", "bottle", "cup", "potted plant", "book"]

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

# ─────────────────────────────
# Vision System Class
# ─────────────────────────────
class VisionSystem:
    def __init__(self, model_path="models/yolov8n_coco_640x352.blob"):
        print("🎥 Initializing Vision System...")
        self.model_path = model_path
        self.pipeline = self.create_pipeline()
        self.device = dai.Device(self.pipeline)
        self.q_rgb = self.device.getOutputQueue("rgb", maxSize=4, blocking=False)
        self.q_det = self.device.getOutputQueue("detections", maxSize=4, blocking=False)
        self._z_ema = {}

    # ─────────────────────────────
    # Create pipeline
    # ─────────────────────────────
    def create_pipeline(self):
        print("🔧 Building DepthAI pipeline...")
        pipeline = dai.Pipeline()

        # Handle version compatibility
        dai_version = getattr(dai, "__version__", "unknown")
        print(f"📦 DepthAI version: {dai_version}")

        # Choose camera creation method based on version
        if dai_version.startswith("3."):
            cam_rgb = pipeline.createCamera()
            cam_rgb.setCamId(0)
        else:
            cam_rgb = pipeline.createColorCamera()
            cam_rgb.setPreviewSize(640, 352)
            cam_rgb.setInterleaved(False)
            cam_rgb.setFps(30)

        # Depth + stereo setup
        monoL = pipeline.createMonoCamera()
        monoR = pipeline.createMonoCamera()
        monoL.setBoardSocket(dai.CameraBoardSocket.LEFT)
        monoR.setBoardSocket(dai.CameraBoardSocket.RIGHT)
        monoL.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)
        monoR.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)

        stereo = pipeline.createStereoDepth()
        stereo.setLeftRightCheck(True)
        stereo.setSubpixel(True)
        stereo.setDepthAlign(dai.CameraBoardSocket.RGB)
        monoL.out.link(stereo.left)
        monoR.out.link(stereo.right)

        # YOLOv8 Spatial Detection
        detection_nn = pipeline.create(dai.node.SpatialDetectionNetwork)

        detection_nn.setBlobPath(self.model_path)
        detection_nn.setConfidenceThreshold(0.4)
        detection_nn.setNumClasses(80)
        detection_nn.setCoordinateSize(4)
        detection_nn.setIouThreshold(0.5)
        detection_nn.setBoundingBoxScaleFactor(0.5)
        detection_nn.setDepthLowerThreshold(100)
        detection_nn.setDepthUpperThreshold(4000)
        detection_nn.input.setBlocking(False)

        # Link RGB to NN
        if hasattr(cam_rgb, "preview"):
            cam_rgb.preview.link(detection_nn.input)
        else:
            cam_rgb.video.link(detection_nn.input)
        stereo.depth.link(detection_nn.inputDepth)

        # Output queues
        xout_rgb = pipeline.createXLinkOut()
        xout_rgb.setStreamName("rgb")
        detection_nn.passthrough.link(xout_rgb.input)

        xout_nn = pipeline.createXLinkOut()
        xout_nn.setStreamName("detections")
        detection_nn.out.link(xout_nn.input)

        return pipeline

    # ─────────────────────────────
    # Run the vision system
    # ─────────────────────────────
    def run(self):
        print("🚀 Starting detection... Press Q to exit (if GUI available).")
        headless = not hasattr(cv2, "imshow")

        while True:
            in_rgb = self.q_rgb.tryGet()
            in_det = self.q_det.tryGet()

            if not in_rgb:
                continue

            frame = in_rgb.getCvFrame()

            if in_det is not None:
                for det in in_det.detections:
                    label = LABEL_MAP[det.label]
                    if label not in TARGET_LABELS:
                        continue

                    depth_m = det.spatialCoordinates.z / 1000.0
                    conf = det.confidence * 100
                    print(f"[Detection] {label}: {conf:.1f}% — {depth_m:.2f} m away")

            if not headless:
                cv2.imshow("Vision Detection", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                time.sleep(0.05)  # Headless mode delay

        if not headless:
            cv2.destroyAllWindows()
        print("🛑 Vision stopped.")

# ─────────────────────────────
# Main
# ─────────────────────────────
if __name__ == "__main__":
    vision = VisionSystem()
    vision.run()
