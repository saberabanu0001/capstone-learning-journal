import depthai as dai
import cv2
import numpy as np
import time

# Target labels you want to detect
# TARGET_LABELS = [
#     "person", "cell phone", "bottle", "cup", "potted plant", "pen", "doll"
# ]

TARGET_LABELS = ["person", "cell phone", "bottle", "cup", "pen", "potted plant", "sports ball", "toy"]


# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
cam_rgb = pipeline.createColorCamera()
spatial_detection_network = pipeline.createYoloSpatialDetectionNetwork()
mono_left = pipeline.createMonoCamera()
mono_right = pipeline.createMonoCamera()
stereo = pipeline.createStereoDepth()

xout_rgb = pipeline.createXLinkOut()
xout_nn = pipeline.createXLinkOut()

xout_rgb.setStreamName("preview")
xout_nn.setStreamName("detections")

# Camera properties
cam_rgb.setPreviewSize(640, 352)
cam_rgb.setInterleaved(False)
cam_rgb.setFps(30)
cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)

# Mono cameras
mono_left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
mono_left.setBoardSocket(dai.CameraBoardSocket.LEFT)
mono_right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
mono_right.setBoardSocket(dai.CameraBoardSocket.RIGHT)

# Stereo depth
stereo.setConfidenceThreshold(255)
stereo.setDepthAlign(dai.CameraBoardSocket.RGB)
stereo.setOutputSize(mono_left.getResolutionWidth(), mono_left.getResolutionHeight())

# YOLO network setup
spatial_detection_network.setBlobPath("models/yolov8n_coco_640x352.blob")
spatial_detection_network.setConfidenceThreshold(0.45)
spatial_detection_network.input.setBlocking(False)
spatial_detection_network.setBoundingBoxScaleFactor(0.5)
spatial_detection_network.setDepthLowerThreshold(100)
spatial_detection_network.setDepthUpperThreshold(5000)

# YOLO-specific parameters
spatial_detection_network.setNumClasses(80)
spatial_detection_network.setCoordinateSize(4)
spatial_detection_network.setAnchors([])
spatial_detection_network.setAnchorMasks({})
spatial_detection_network.setIouThreshold(0.5)

# Link nodes
cam_rgb.preview.link(spatial_detection_network.input)
mono_left.out.link(stereo.left)
mono_right.out.link(stereo.right)
stereo.depth.link(spatial_detection_network.inputDepth)
spatial_detection_network.passthrough.link(xout_rgb.input)
spatial_detection_network.out.link(xout_nn.input)

# Load COCO labels
LABEL_MAP = [
    "person","bicycle","car","motorcycle","airplane","bus","train","truck","boat","traffic light",
    "fire hydrant","stop sign","parking meter","bench","bird","cat","dog","horse","sheep","cow",
    "elephant","bear","zebra","giraffe","backpack","umbrella","handbag","tie","suitcase","frisbee",
    "skis","snowboard","sports ball","kite","baseball bat","baseball glove","skateboard","surfboard","tennis racket",
    "bottle","wine glass","cup","fork","knife","spoon","bowl","banana","apple","sandwich","orange","broccoli",
    "carrot","hot dog","pizza","donut","cake","chair","couch","potted plant","bed","dining table","toilet","tv",
    "laptop","mouse","remote","keyboard","cell phone","microwave","oven","toaster","sink","refrigerator",
    "book","clock","vase","scissors","teddy bear","hair drier","toothbrush"
]

# Start the pipeline
with dai.Device(pipeline) as device:
    preview_q = device.getOutputQueue(name="preview", maxSize=4, blocking=False)
    detection_q = device.getOutputQueue(name="detections", maxSize=4, blocking=False)

    start_time = time.time()
    frame_count = 0

    while True:
        in_preview = preview_q.get()
        in_det = detection_q.tryGet()

        frame = in_preview.getCvFrame()
        frame_count += 1

        if in_det:
            detections = in_det.detections
            for det in detections:
                label = LABEL_MAP[det.label]
                if label in TARGET_LABELS:
                    x1 = int(det.xmin * frame.shape[1])
                    y1 = int(det.ymin * frame.shape[0])
                    x2 = int(det.xmax * frame.shape[1])
                    y2 = int(det.ymax * frame.shape[0])

                    depth = det.spatialCoordinates.z / 1000  # mm → meters
                    conf = det.confidence * 100

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{label} {conf:.1f}% ({depth:.2f}m)",
                                (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (255, 255, 255), 2)
                    print(f"[Vision] {label} ({conf:.1f}%) - {depth:.2f} m away")

        cv2.imshow("Vision Detection", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    end_time = time.time()
    print(f"✅ Vision module test complete. ({frame_count / (end_time - start_time):.2f} FPS)")
