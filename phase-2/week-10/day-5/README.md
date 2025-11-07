# 🧠 LLaVA Vision-Language Model – Troubleshooting Report

This document summarizes the issues encountered while integrating the LLaVA (Large Language and Vision Assistant) model for real-time webcam captioning as part of the capstone robot vision module.

## ⚙️ Overview

LLaVA was implemented to enable the robot’s camera system to interpret visual scenes and describe them in natural language. The model was tested on a MacBook M4 (16 GB RAM) using the Hugging Face Transformers and Torch frameworks.

## 🚨 Problems Faced
- 1. Model Loading Error

The model llava-hf/llava-v1.5-7b-hf could not be fetched from Hugging Face.

- - Error:

OSError: llava-hf/llava-v1.5-7b-hf is not a valid model identifier
RepositoryNotFoundError: processor_config.json not found


Cause: Model name changed or requires a private-access token.

- 2. Hardware Limitation

The 7B parameter model required high GPU memory.

On CPU-only MacBook, model loading took 5–7 minutes and froze during inference.

This made real-time captioning impossible.

- 3. Frame Processing Instability

Continuous webcam input caused repeated frames to be sent to the model.

Resulted in:

Duplicate descriptions

Base64 decoding errors

Irrelevant or unstable text output

## 🧩 Planned Fixes (Next Week)

- Switch to LLaVA-Lightning or BLIP2 for lightweight inference.

- Optimize frame capture loop to process one image every 2–3 seconds.

- Move inference to Jetson Orin NX for faster GPU-based execution.

- Rebuild environment with latest libraries:

***transformers>=4.45.0***
***torch>=2.2.0***
***huggingface_hub>=0.23.0***
***accelerate***
***pillow***
***opencv-python***

## 🧪 Test Plan

- Run LLaVA inference with static images first (test_image.jpg).

- Extend to live webcam input after verifying model stability.

- Integrate voice (TTS) and SLAM modules for full robotic demonstration.

- 📸 Output Example (Expected)

“A person standing near a robotic platform with a mounted projector.”