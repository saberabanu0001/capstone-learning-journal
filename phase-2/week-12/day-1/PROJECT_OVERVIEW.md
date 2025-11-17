# Rovy AI Smart Robot - Complete Project Overview

## 🧠 System Overview

**Jetson Nano = The Powerful Brain** 🧠
- Runs all Python code, AI models (LLaVA), vision processing, and decision-making
- Handles stereo depth analysis, speech recognition, and navigation logic
- GPU-accelerated AI inference

**ESP32 = Motor Controller Base**
- Simple microcontroller that receives motor commands
- Handles low-level motor control, sensors, and hardware
- Just executes commands from Jetson Nano

---

## 🤖 What is Rovy?

Rovy is an **autonomous AI-powered robot** that combines:
- **Brain**: Jetson Nano (powerful AI computer) - runs everything
- **Vision**: Oak-D stereo depth camera for 3D perception
- **AI Understanding**: LLaVA vision-language model for scene understanding
- **Voice Control**: ReSpeaker microphone array + speech recognition
- **Movement**: ESP32-based rover base (motor controller)
- **Smart Assistant**: Natural language interaction with voice commands

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    JETSON NANO - THE BRAIN 🧠                    │
│              (Powerful AI Computer - Runs Everything)            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              PYTHON SOFTWARE STACK                        │  │
│  │                                                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │   VISION     │  │     AI       │  │   VOICE      │  │  │
│  │  │   SYSTEM     │  │  ASSISTANT   │  │  ASSISTANT   │  │  │
│  │  │              │  │              │  │              │  │  │
│  │  │ • Oak-D      │  │ • LLaVA      │  │ • ReSpeaker  │  │  │
│  │  │   Camera     │  │   Model      │  │   Mic Array  │  │  │
│  │  │ • Depth      │  │ • Vision-    │  │ • Speech     │  │  │
│  │  │   Analysis   │  │   Language   │  │   Recognition│  │  │
│  │  │ • 3D         │  │ • Scene      │  │ • TTS        │  │  │
│  │  │   Perception │  │   Understanding│ │             │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ USB Serial
                              │ (Motor Commands)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              ESP32 ROVER BASE - Motor Controller                 │
│              (Low-level Hardware - Just Executes Commands)       │
│                                                                  │
│  • Motors (Left/Right wheels)                                   │
│  • OLED Display                                                 │
│  • IMU Sensor (orientation)                                     │
│  • Battery Monitor                                              │
│  • Camera Gimbal (pan/tilt)                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure & File Connections

### **Core Components:**

#### 1. **`rover_controller.py`** - Hardware Interface
- **Purpose**: Communication bridge between Jetson Nano (brain) and ESP32 rover base
- **What it does**:
  - Sends motor commands from Jetson → ESP32 via serial (JSON format: `{"T":1,"L":0.5,"R":0.5}`)
  - Reads sensor feedback from ESP32 → Jetson (battery, IMU, wheel speeds)
  - Controls OLED display on rover
  - Controls camera gimbal (pan/tilt) on rover
- **Runs on**: Jetson Nano (the brain)
- **Communicates with**: ESP32 (motor controller)
- **Used by**: All navigation and assistant scripts

#### 2. **`oakd_depth_navigator.py`** - Vision System (YOUR AREA!)
- **Purpose**: 3D depth perception and obstacle avoidance
- **Components**:
  - `OakDDepthCamera`: Captures RGB + depth frames from Oak-D camera
  - `DepthNavigator`: Analyzes depth maps to find safe paths
- **Key Features**:
  - Stereo depth at 30 FPS
  - Divides view into 5 regions (far_left, left, center, right, far_right)
  - Calculates clearance scores for each region
  - Returns navigation commands: `forward`, `left`, `right`, `stop`
- **Used by**: `depth_llava_nav.py` (autonomous navigation)

#### 3. **`llava_cpp_navigator.py`** - AI Scene Understanding
- **Purpose**: High-level scene understanding using LLaVA vision-language model
- **What it does**:
  - Takes RGB images
  - Uses LLaVA to understand the scene
  - Provides strategic navigation guidance
- **Used by**: `depth_llava_nav.py` (combines with depth for smart navigation)

#### 4. **`depth_llava_nav.py`** - Autonomous Navigation System
- **Purpose**: Combines depth perception + AI for autonomous movement
- **How it works**:
  ```
  1. Camera Thread: Captures frames at 30 FPS → puts in queue
  2. LLaVA Thread: Analyzes scenes every 15s → provides strategic guidance
  3. Depth Thread: Real-time obstacle avoidance at 20 FPS → executes movement
  ```
- **Decision Logic**:
  - Depth system handles immediate obstacles (safety-first)
  - LLaVA provides high-level guidance (e.g., "go toward door")
  - Combines both: follows LLaVA if depth confirms it's safe

#### 5. **`smart_assistant.py`** - Voice-Controlled Assistant
- **Purpose**: Natural language interaction with the robot
- **Components**:
  - `ReSpeakerInterface`: Voice input (microphone array)
  - `LLaVaAssistant`: AI brain (text + vision questions)
  - `TextToSpeech`: Voice output (Piper TTS or espeak)
  - `SmartAssistant`: Main orchestrator
- **Features**:
  - Wake word detection ("hey rovy", "hey rover")
  - Voice commands for movement ("go forward", "turn left")
  - Vision questions ("what do you see?")
  - Can start/stop autonomous navigation
- **Uses**: `rover_controller.py` for movement, camera for vision

---

## 🔄 Data Flow Diagrams

### **Autonomous Navigation Flow** (`depth_llava_nav.py`):

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS NAVIGATION                      │
└─────────────────────────────────────────────────────────────┘

Thread 1: Camera Capture (30 FPS)
    │
    ├─> Oak-D Camera captures RGB + Depth
    │
    └─> Frame Queue (max 2 frames)
            │
            ├─────────────────┬─────────────────┐
            │                 │                 │
            ▼                 ▼                 ▼
    Thread 2: LLaVA        Thread 3: Depth Navigation
    (Every 15s)            (20 FPS - Real-time)
            │                 │
            │                 ├─> Analyze depth map
            │                 │   • 5 regions (left/center/right)
            │                 │   • Calculate clearance scores
            │                 │   • Safety-first decision
            │                 │
            ├─> Scene        │
            │   Analysis     │
            │   • "What do   │
            │     I see?"    │
            │   • Strategic  │
            │     guidance   │
            │                 │
            └───────┬─────────┘
                    │
                    ▼
            Combine Guidance
            • Depth = immediate safety
            • LLaVA = strategic direction
                    │
                    ▼
            Motor Commands
            • forward/left/right/stop
            • Speed based on clearance
                    │
                    ▼
            ESP32 Rover
            • Executes movement
```

### **Voice Assistant Flow** (`smart_assistant.py`):

```
┌─────────────────────────────────────────────────────────────┐
│                    VOICE ASSISTANT                          │
└─────────────────────────────────────────────────────────────┘

User speaks
    │
    ▼
ReSpeaker Microphone
    │
    ▼
Speech Recognition (Google API)
    │
    ├─> Wake word? ("hey rovy")
    │   └─> Activate assistant
    │
    └─> Question/Command
            │
            ├─────────────────┬─────────────────┐
            │                 │                 │
            ▼                 ▼                 ▼
    Movement Command?    Vision Question?   General Question?
            │                 │                 │
            │                 │                 │
    Execute Movement      Capture Image      Text-only
    (via rover_controller)  │                 │
                            │                 │
                            ▼                 ▼
                    LLaVA Analysis      LLaVA Analysis
                    (with image)        (text only)
                            │                 │
                            └────────┬────────┘
                                     │
                                     ▼
                            Generate Response
                                     │
                                     ▼
                            Text-to-Speech
                            (Piper/espeak)
                                     │
                                     ▼
                            User hears response
```

---

## 🎯 Vision System Deep Dive (Your Area!)

### **`oakd_depth_navigator.py` - How It Works:**

#### **1. OakDDepthCamera Class**
```python
# Initialization
camera = OakDDepthCamera(resolution=(640, 480))
camera.start()

# Captures two streams:
rgb_frame, depth_frame = camera.capture_frames()
# - rgb_frame: Color image (640x480)
# - depth_frame: Depth map in millimeters (640x480)
```

**What happens inside:**
- Creates DepthAI pipeline
- Configures RGB camera (640x480)
- Configures stereo cameras (left + right for depth)
- Stereo matching → depth map
- Outputs both via queues

#### **2. DepthNavigator Class**
```python
navigator = DepthNavigator(safe_distance_mm=800)
command = navigator.get_navigation_command(rgb_frame, depth_frame)
```

**Decision Process:**

```
Step 1: Extract Middle Strip (35%-65% of height)
    ┌─────────────────────────────┐
    │  (ignored - sky/ceiling)    │ ← Top 35%
    ├─────────────────────────────┤
    │  ╔═══════════════════════╗  │ ← Middle strip (analyzed)
    │  ║ L │ L │ C │ R │ R ║  │     (obstacles at robot height)
    │  ╚═══════════════════════╝  │
    ├─────────────────────────────┤
    │  (ignored - ground)         │ ← Bottom 35%
    └─────────────────────────────┘

Step 2: Divide into 5 Regions
    ┌──────┬──────┬──────┬──────┬──────┐
    │ Far  │ Left │Center│ Right│ Far  │
    │ Left │      │      │      │ Right│
    └──────┴──────┴──────┴──────┴──────┘

Step 3: Calculate Clearance Score for Each
    - Filter valid depths (0 < depth < 5000mm)
    - Calculate median distance
    - Score: 0.0 (blocked) to 1.0 (clear)
    - Formula: Linear mapping from 400mm (min) to 2000mm (max)

Step 4: Safety-First Decision
    - Only consider regions with score ≥ 0.35 (safety threshold)
    - If forward is safe AND competitive → go forward
    - If forward blocked → choose best side (left/right)
    - If all blocked → random turn to explore

Step 5: Speed Adjustment
    - High clearance (>0.8) → slow speed (0.3m)
    - Medium clearance (0.6-0.8) → slow speed (0.2m)
    - Low clearance (<0.6) → very slow (0.15m)
```

**Output Format:**
```python
{
    'action': 'forward',  # or 'left', 'right', 'stop'
    'speed': 'slow',
    'distance': 0.3,
    'reasoning': 'Forward safe & competitive (C=75% ≥ 85% of best=80%)',
    'scores': {
        'far_left': 0.6,
        'left': 0.7,
        'center': 0.75,  # Best path
        'right': 0.65,
        'far_right': 0.5
    }
}
```

---

## 🔌 How Components Connect

### **Connection Map:**

```
┌──────────────────────────────────────────────────────────────┐
│         JETSON NANO - The Powerful Brain 🧠                   │
│         (Runs all AI, vision processing, Python code)         │
└──────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
USB Port 1:              USB Port 2:            USB Port 3:
Oak-D Camera             ESP32 Rover             ReSpeaker Mic
    │                    (Serial)                    │
    │                        │                       │
    └─> depthai          pyserial              PyAudio
        library               │                       │
        │                    │                       │
        ▼                    ▼                       ▼
oakd_depth_navigator.py  rover_controller.py  smart_assistant.py
        │                    │                       │
        │                    └─> JSON commands      │
        │                    {"T":1,"L":0.5,"R":0.5} │
        │                                             │
        └───────────────────────────────────────────┘
                              │
                              ▼
                    USB Port 4: USB Speakers
                              │
                              └─> aplay (TTS output)
```

**Key Point**: All Python code, AI models, and vision processing run on the **Jetson Nano**. The ESP32 is just a motor controller that receives commands.

### **Software Connections:**

```
smart_assistant.py
    │
    ├─> Uses rover_controller.py (Rover class)
    │   └─> For movement commands
    │
    ├─> Uses oakd_depth_navigator.py (OakDDepthCamera)
    │   └─> For vision questions ("what do you see?")
    │
    └─> Uses llava_cpp_navigator.py (LLaVACppNavigator)
        └─> For AI understanding

depth_llava_nav.py
    │
    ├─> Uses rover_controller.py (Rover class)
    │   └─> For motor control
    │
    ├─> Uses oakd_depth_navigator.py
    │   ├─> OakDDepthCamera (frame capture)
    │   └─> DepthNavigator (obstacle avoidance)
    │
    └─> Uses llava_cpp_navigator.py (LLaVACppNavigator)
        └─> For strategic guidance
```

---

## 🚀 Running the System

### **1. Autonomous Navigation** (Vision + AI):
```bash
python depth_llava_nav.py --duration 300 --safe-distance 800
```
- Runs for 300 seconds
- Combines depth perception + LLaVA AI
- Navigates autonomously

### **2. Voice Assistant**:
```bash
python smart_assistant.py --port /dev/ttyACM0
```
- Listens for wake word ("hey rovy")
- Responds to questions
- Can control movement via voice

### **3. Status Display**:
```bash
python display_status.py --mode simple
```
- Shows battery, temperature, status on OLED

---

## 🎨 Key Design Patterns

### **1. Threading Architecture** (`depth_llava_nav.py`):
- **Producer-Consumer**: Camera thread produces frames → queue → navigation thread consumes
- **Thread Safety**: Uses `threading.Lock()` for shared LLaVA guidance
- **Non-blocking**: LLaVA loads in background, doesn't block startup

### **2. Safety-First Navigation**:
- Depth system has priority (immediate safety)
- LLaVA provides suggestions, but depth must confirm
- Emergency stops if clearance drops suddenly

### **3. Modular Design**:
- Each component is independent
- Can run vision-only, assistant-only, or combined
- Easy to test individual components

---

## 🔧 Recent Changes (What Team Leader Modified)

Based on code analysis, likely changes:

1. **Removed `rotate_and_scan` function** from `DepthNavigator`
   - Comment says: "It conflicted with _capture_thread"
   - Now uses continuous frame capture instead

2. **Frame Queue System** in `depth_llava_nav.py`
   - Single capture thread feeds multiple consumers
   - Prevents conflicts between LLaVA and depth navigation

3. **Thread-Safe LLaVA Guidance**
   - Uses `threading.Lock()` to protect shared state
   - Prevents race conditions

4. **Emergency Stop Logic**
   - Detects sudden clearance drops
   - Prevents collisions

---

## 📊 Vision System Parameters

### **DepthNavigator Settings:**
- `safe_distance_mm`: 800mm (default) - minimum safe distance
- `warning_distance_mm`: 1200mm (1.5x safe) - early warning
- `blocked_distance_mm`: 600mm (0.75x safe) - too close

### **Region Analysis:**
- Middle strip: 35%-65% of image height (robot-height obstacles)
- 5 regions: far_left, left, center, right, far_right
- Safety threshold: 0.35 (35% clearance minimum)

### **Speed Control:**
- Always "slow" for safety
- Distance: 0.15m - 0.3m based on clearance
- Emergency stop if clearance drops >30%

---

## 🐛 Debugging Tips

### **Vision Issues:**
1. Check Oak-D camera connection: `lsusb | grep DepthAI`
2. Test camera: Run `oakd_depth_navigator.py` standalone
3. Check depth values: Print median distances in each region

### **Navigation Issues:**
1. Check rover connection: `ls /dev/ttyACM*`
2. Test motors: Use `rover_controller.py` directly
3. Check frame queue: Monitor queue size in `depth_llava_nav.py`

### **AI Issues:**
1. Check LLaVA model paths in `llava_cpp_navigator.py`
2. Monitor GPU memory: `nvidia-smi`
3. Check inference time: Should be <5s per analysis

---

## 📝 Summary

**Your Vision System (`oakd_depth_navigator.py`):**
- Captures RGB + depth from Oak-D camera
- Analyzes depth map for obstacles
- Returns safe navigation commands
- Used by autonomous navigation system

**How It All Fits:**
- Vision provides real-time obstacle avoidance
- AI (LLaVA) provides strategic understanding
- Voice assistant provides user interaction
- Rover controller executes all movement commands

**Key Insight:**
The system uses a **two-layer approach**:
1. **Reactive Layer** (Depth): Fast, safety-first obstacle avoidance
2. **Strategic Layer** (LLaVA): High-level scene understanding and planning

Both work together for intelligent autonomous navigation!

