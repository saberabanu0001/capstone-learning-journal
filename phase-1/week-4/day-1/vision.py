import depthai as dai
import cv2
import numpy as np

class VisionSystem:
    def __init__(self):
        # Build the pipeline
        self.pipeline = dai.Pipeline()
        
        # RGB camera node
        self.cam = self.pipeline.create(dai.node.ColorCamera)
        self.cam.setPreviewSize(300, 300)
        self.cam.setInterleaved(False)
        
        # XLink output
        xout = self.pipeline.create(dai.node.XLinkOut)
        xout.setStreamName("rgb")
        self.cam.preview.link(xout.input)
        
        # Start device
        self.device = dai.Device(self.pipeline)
        self.q_rgb = self.device.getOutputQueue("rgb")

    def get_latest_frame(self):
        # To be implemented Day-2
        pass

    def get_center_depth(self):
        # To be implemented Day-3
        pass
