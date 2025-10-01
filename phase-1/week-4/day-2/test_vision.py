import sys
import os

# Go up 3 levels to project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from modules.vision import VisionSystem

import cv2

vision = VisionSystem()

while True:
    frame = vision.get_latest_frame()
    cv2.imshow("Live Feed", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
