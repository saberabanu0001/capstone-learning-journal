# 📅 Week 6 – Day 3: Mock Integration (Vision + Audio)
## 🎯 Objective

Simulate integration between the Vision module (handled by Sabera) and the Audio module (handled by another team member).
Since the audio hardware is not available yet, a mock integration is created to demonstrate how both modules will communicate in the real system.

## ⚙️ Task Overview

- Create a mock file test_integration_mock.py.

- Use the VisionSystem (simulation mode) to generate detections.

- For each detection, simulate an audio feedback response (text-based mock).

- This test demonstrates communication readiness between the two systems.

## 🧠 Key Functions Used

- VisionSystem.get_detections_with_depth() → simulates detection of objects (person, car, dog, etc.)

- simulate_audio_response(label, distance) → mimics audio output messages for detected objects.