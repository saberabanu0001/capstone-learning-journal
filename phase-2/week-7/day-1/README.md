# 🧠 Capstone Robotics — Jetson Remote Setup via Tailscale (OAK-D Lite)
## Overview

**This guide documents how Sabera Banu connected her MacBook Air to the Jetson (Ubuntu) board remotely using Tailscale, verified the DepthAI setup, and confirmed successful camera operation of the OAK-D Lite module.**

## 🛰️ 1. Remote Connection Setup (Tailscale)
### ✅ What We Used:

- Tailscale for private VPN connection (Mac ↔ Jetson).

- Shared team account: rovercapstone@gmail.com

- Password (team-shared): **********

- Three connected devices:

- bakhtiyors-mac-mini

- saberas-macbook-air

- ubuntu (Jetson board)





## ⚙️ Setup Steps:

- Installed Tailscale on both Mac and Jetson.

- Logged in using the shared Tailscale account (rovercapstone@gmail.com).

- Verified connection on Tailscale Admin Panel:

- - All machines showed as Connected (green dot ✅).

- SSH connection was established from Mac to Jetson:

- - - ssh root@100.87.198.86


- Confirmed successful connection with:

- - Welcome to Ubuntu 20.04.6 LTS (Jetson)




## 2. OAK-D Lite Connection Verification
### 🧩 Step 1: Check if the camera is connected
- - lsusb


Output confirmed device:

- - Bus 001 Device 011: ID 03e7:2485 Intel Movidius MyriadX

### 🧩 Step 2: Install DepthAI SDK
- sudo apt install python3-pip python3-dev python3-numpy -y
- pip3 install depthai==2.29.0.0


### ✅ Success: Installed precompiled wheel for ARM (aarch64).




## 🧠 3. DepthAI Test (Camera Verification)
🔧 Created Test Script: test_depthai.py
import depthai as dai

pipeline = dai.Pipeline()
cam_rgb = pipeline.createColorCamera()
xout = pipeline.createXLinkOut()
xout.setStreamName("video")
cam_rgb.video.link(xout.input)

with dai.Device(pipeline) as device:
    print("Device connected:", device.getDeviceName())
    q = device.getOutputQueue(name="video", maxSize=4, blocking=False)
    while True:
        frame = q.get().getCvFrame()
        print("Frame received:", frame.shape)
        break

## ▶️ Run the Test:
***python3 test_depthai.py***

## ✅ Output:
***Device connected: OAK-D-LITE***
***Frame received: (1080, 1920, 3)***


## ✅ This confirms:

- DepthAI SDK works.

- Jetson recognizes and streams from OAK-D Lite camera.

- Python can access the video frames successfully.
