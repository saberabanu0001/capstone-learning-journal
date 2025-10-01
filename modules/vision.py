class VisionSystem:
    def __init__(self):
        """
        Initialize the pipeline (RGB, Depth, NN).
        """
        pass
    
    def get_rgb_frame(self):
        """
        Return the latest RGB frame.
        In future: this will call DepthAI's queue and fetch frames.
        """
        pass

    def get_depth_map(self):
        """
        Return the latest depth map.
        In future: will process StereoDepth output.
        """
        pass

    def get_detections(self):
        """
        Return a list of detections:
        [ {label: 'person', confidence: 0.91, x: 20, y: 200, z: 2400}, ... ]
        """
        pass
    
    def is_person_detected(self):
        """
        Helper function for Motion team.
        Returns True if 'person' is detected, else False.
        """
        pass
