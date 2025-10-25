import depthai as dai
import cv2
import numpy as np
import os
import subprocess

# ─────────────── MODEL & LABELS ───────────────
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "yolov8n_coco_640x352.blob"))
TARGET_LABELS = ["person", "bottle", "cup", "cell phone", "potted plant"]

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

# ─────────────── VISION SYSTEM ───────────────
class VisionSystem:
    def __init__(self):
        print("🎥 Initializing OAK-D Lite Vision System (DepthAI v2.30.0.0)…")
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"❌ Model not found at {MODEL_PATH}")
        self.pipeline = self.create_pipeline()
        self._z_ema = {}
        self._last_spoken = {}

    def create_pipeline(self):
        print("🔧 Building DepthAI pipeline (YOLOv8n @ 640x352)…")
        pipeline = dai.Pipeline()

        # RGB Camera
        cam_rgb = pipeline.create(dai.node.ColorCamera)
        cam_rgb.setPreviewSize(640, 352)
        cam_rgb.setInterleaved(False)
        cam_rgb.setFps(30)

        # Mono Cameras
        monoL = pipeline.create(dai.node.MonoCamera)
        monoR = pipeline.create(dai.node.MonoCamera)
        monoL.setBoardSocket(dai.CameraBoardSocket.CAM_B)
        monoR.setBoardSocket(dai.CameraBoardSocket.CAM_C)
        monoL.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)
        monoR.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)

        stereo = pipeline.create(dai.node.StereoDepth)
        stereo.setLeftRightCheck(True)
        stereo.setSubpixel(True)
        stereo.setDepthAlign(dai.CameraBoardSocket.CAM_A)
        monoL.out.link(stereo.left)
        monoR.out.link(stereo.right)

        # YOLO Detection Network
        det = pipeline.create(dai.node.YoloSpatialDetectionNetwork)
        det.setBlobPath(MODEL_PATH)
        det.setConfidenceThreshold(0.45)
        det.setNumClasses(len(LABEL_MAP))
        det.setCoordinateSize(4)
        det.setIouThreshold(0.5)
        det.setDepthLowerThreshold(100)
        det.setDepthUpperThreshold(4000)
        det.setBoundingBoxScaleFactor(0.5)
        cam_rgb.preview.link(det.input)
        stereo.depth.link(det.inputDepth)

        # Output Streams
        xout_rgb = pipeline.create(dai.node.XLinkOut)
        xout_rgb.setStreamName("rgb")
        cam_rgb.preview.link(xout_rgb.input)  # FIXED → direct RGB feed

        xout_det = pipeline.create(dai.node.XLinkOut)
        xout_det.setStreamName("detections")
        det.out.link(xout_det.input)

        return pipeline

    def run(self):
        print("✅ Starting detection… Press Q to quit.")
        with dai.Device(self.pipeline) as device:
            q_rgb = device.getOutputQueue("rgb", 4, False)
            q_det = device.getOutputQueue("detections", 4, False)

            while True:
                in_rgb = q_rgb.tryGet()
                in_det = q_det.tryGet()

                if in_rgb is not None:
                    frame = in_rgb.getCvFrame()

                    if in_det is not None:
                        for det in in_det.detections:
                            if det.label >= len(LABEL_MAP):
                                continue
                            label = LABEL_MAP[det.label]
                            if label not in TARGET_LABELS:
                                continue

                            x1, y1 = int(det.xmin * frame.shape[1]), int(det.ymin * frame.shape[0])
                            x2, y2 = int(det.xmax * frame.shape[1]), int(det.ymax * frame.shape[0])
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                            conf = det.confidence * 100
                            depth_m = det.spatialCoordinates.z / 1000.0
                            text = f"{label} {conf:.1f}% ({depth_m:.2f}m)"
                            cv2.putText(frame, text, (x1, max(y1 - 10, 20)),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                            print(f"[Vision] {label} ({conf:.1f}%) – {depth_m:.2f} m away")

                            # Voice feedback (only once every few seconds per label)
                            if conf > 70 and (label not in self._last_spoken or 
                                             (cv2.getTickCount() - self._last_spoken[label]) / cv2.getTickFrequency() > 4):
                                phrase = f"{label} detected {depth_m:.1f} meters away."
                                subprocess.Popen(['say', phrase])
                                self._last_spoken[label] = cv2.getTickCount()

                    cv2.imshow("Vision Detection", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cv2.destroyAllWindows()
            print("🛑 Stopped. ✅ Vision module complete.")


if __name__ == "__main__":
    VisionSystem().run()
