import depthai as dai
import cv2
import numpy as np
import threading
import time
import os
from modules.vision_face import FaceRecognition

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "yolov8n_coco_640x352.blob"))
TARGET_LABELS = ["person"]

LABEL_MAP = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
             "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
             "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
             "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
             "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
             "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
             "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
             "sofa", "potted plant", "bed", "dining table", "toilet", "tvmonitor", "laptop", "mouse",
             "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator",
             "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

class VisionSystem:
    def __init__(self):
        print("🎥 Initializing OAK-D Vision System with Face Recognition…")
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

        self.pipeline = self.create_pipeline()
        self.device = dai.Device(self.pipeline)
        self.q_rgb = self.device.getOutputQueue("rgb", maxSize=8, blocking=False)
        self.q_det = self.device.getOutputQueue("detections", maxSize=8, blocking=False)

        self.face_recognizer = FaceRecognition()
        self.frame = None
        self.detections = []
        self.lock = threading.Lock()
        self.last_print = time.time()

    def create_pipeline(self):
        p = dai.Pipeline()

        cam_rgb = p.createColorCamera()
        cam_rgb.setPreviewSize(640, 352)
        cam_rgb.setInterleaved(False)
        cam_rgb.setPreviewKeepAspectRatio(False)
        cam_rgb.setFps(30)

        monoL = p.createMonoCamera()
        monoR = p.createMonoCamera()
        monoL.setBoardSocket(dai.CameraBoardSocket.LEFT)
        monoR.setBoardSocket(dai.CameraBoardSocket.RIGHT)
        monoL.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        monoR.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)

        stereo = p.createStereoDepth()
        stereo.setDepthAlign(dai.CameraBoardSocket.RGB)
        stereo.setSubpixel(True)
        stereo.setLeftRightCheck(True)
        monoL.out.link(stereo.left)
        monoR.out.link(stereo.right)

        det = p.createYoloSpatialDetectionNetwork()
        det.setBlobPath(MODEL_PATH)
        det.setConfidenceThreshold(0.4)
        det.setNumClasses(80)
        det.setCoordinateSize(4)
        det.setIouThreshold(0.5)
        det.setDepthLowerThreshold(100)
        det.setDepthUpperThreshold(4000)
        cam_rgb.preview.link(det.input)
        stereo.depth.link(det.inputDepth)

        xout_rgb = p.createXLinkOut()
        xout_rgb.setStreamName("rgb")
        det.passthrough.link(xout_rgb.input)

        xout_nn = p.createXLinkOut()
        xout_nn.setStreamName("detections")
        det.out.link(xout_nn.input)

        return p

    def update_detections(self):
        while True:
            in_det = self.q_det.tryGet()
            if in_det:
                with self.lock:
                    self.detections = in_det.detections

    def run(self):
        print("✅ Starting combined detection… Press Q to quit.")
        threading.Thread(target=self.update_detections, daemon=True).start()

        cv2.namedWindow("Vision Detection", cv2.WINDOW_NORMAL)

        while True:
            in_rgb = self.q_rgb.tryGet()
            if in_rgb:
                frame = in_rgb.getCvFrame()
                frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=20)

                with self.lock:
                    for det in self.detections:
                        if det.label >= len(LABEL_MAP):
                            continue
                        label = LABEL_MAP[det.label]
                        if label not in TARGET_LABELS:
                            continue
                        x1 = int(det.xmin * frame.shape[1])
                        y1 = int(det.ymin * frame.shape[0])
                        x2 = int(det.xmax * frame.shape[1])
                        y2 = int(det.ymax * frame.shape[0])
                        depth_m = det.spatialCoordinates.z / 1000.0
                        conf = det.confidence * 100

                        # Extract ROI for face recognition
                        person_roi = frame[y1:y2, x1:x2]
                        matches = self.face_recognizer.recognize_face(person_roi)

                        for name, (left, top, right, bottom) in matches:
                            cv2.rectangle(person_roi, (left, top), (right, bottom), (255, 0, 0), 2)
                            cv2.putText(person_roi, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                            if name != "Unknown":
                                print(f"🧠 Recognized {name} at {depth_m:.2f} m ")

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 3)
                        cv2.putText(frame, f"{label} {conf:.1f}% ({depth_m:.2f}m)", (x1, max(y1 - 10, 20)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

                cv2.imshow("Vision Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        print("🛑 Stopped. ✅ Vision + Face module complete.")


if __name__ == "__main__":
    VisionSystem().run()
