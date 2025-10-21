

# This system has been minimized by removing packages and content that are
not required on a system that users do not log into.
To restore this content, you can run the 'unminimize' command.
Expanded Security Maintenance for Infrastructure is not enabled.
5 updates can be applied immediately.
4 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable
116 additional security updates can be applied with ESM Infra.
Learn more about enabling ESM Infra service for Ubuntu 20.04 at

Apply Fix 1: Delete the duplicate node creation line around line 79 (the one starting with detection_nn = pipeline.create(dai.node.SpatialDetectionNetwork)).

Apply Fix 2: Delete the debug line print("Detections:", detections) (around line 161).

Save and Exit Nano (Ctrl+X, Y, Enter).

Run the script: