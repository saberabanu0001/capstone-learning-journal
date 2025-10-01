import depthai as dai
import cv2
import numpy as np

class VisionSystem:
    def __init__(self):
        # Create DepthAI pipeline
        self.pipeline = dai.Pipeline()

        # Create color camera
        cam_rgb = self.pipeline.create(dai.node.ColorCamera)
        cam_rgb.setPreviewSize(640, 480)
        cam_rgb.setInterleaved(False)
        cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

        # Create mono cameras (for depth)
        mono_left = self.pipeline.create(dai.node.MonoCamera)
        mono_right = self.pipeline.create(dai.node.MonoCamera)
        stereo = self.pipeline.create(dai.node.StereoDepth)

        mono_left.setBoardSocket(dai.CameraBoardSocket.LEFT)
        mono_right.setBoardSocket(dai.CameraBoardSocket.RIGHT)

        # Output nodes
        xout_rgb = self.pipeline.create(dai.node.XLinkOut)
        xout_depth = self.pipeline.create(dai.node.XLinkOut)
        xout_rgb.setStreamName("rgb")
        xout_depth.setStreamName("depth")

        # Link camera → outputs
        cam_rgb.preview.link(xout_rgb.input)
        mono_left.out.link(stereo.left)
        mono_right.out.link(stereo.right)
        stereo.depth.link(xout_depth.input)

        # Connect to device
        self.device = dai.Device(self.pipeline)
        self.q_rgb = self.device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
        self.q_depth = self.device.getOutputQueue(name="depth", maxSize=4, blocking=False)

    def get_latest_frame(self):
        """Return the latest RGB frame"""
        in_rgb = self.q_rgb.tryGet()
        if in_rgb is not None:
            return in_rgb.getCvFrame()
        return np.zeros((480, 640, 3), dtype=np.uint8)

    def get_center_depth(self):
        """Return depth at the center pixel (in mm)"""
        in_depth = self.q_depth.tryGet()
        if in_depth is not None:
            depth_frame = in_depth.getFrame()
            h, w = depth_frame.shape
            center_value = depth_frame[h//2, w//2]
            return center_value  # in millimeters
        return -1  # if no depth available
