Vision-Language Model (VLM) Live Captioning
# 🎥 Vision-Language Model (VLM) Live Captioning

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white&style=for-the-badge">
  <img src="https://img.shields.io/badge/OpenCV-RealTime-green?logo=opencv&logoColor=white&style=for-the-badge">
  <img src="https://img.shields.io/badge/Hugging Face🤗-Transformers-yellow?style=for-the-badge">
  <img src="https://img.shields.io/badge/PyTorch-Deep Learning-red?logo=pytorch&logoColor=white&style=for-the-badge">
</p>

---

### 🧩 Overview
This project demonstrates a **real-time Vision-Language Model (VLM)** that uses your webcam to describe what it sees in **natural language**.  
It leverages **BLIP (Bootstrapped Language-Image Pretraining)** from Hugging Face to generate captions directly from live video.

---

## 🚀 Features
- 🎥 Real-time video streaming via OpenCV  
- ⚙️ Frame skipping for smoother performance (processes every 60 frames)  
- 🧠 BLIP model for natural-language image captioning  
- 💻 Works on both **MacBook webcam** and **OAK-D camera**  

---

## 🧩 Requirements
Install all dependencies:

***pip install torch torchvision pillow opencv-python transformers accelerate***

---

## ⚙️ How to Run
- ***python test.py***


- The webcam window will open.

- Every few seconds the model will describe what it sees.

- Press 'q' to quit.

---

## 📸 Example Output
- 🧠 Caption: a person sitting at a desk using a laptop  
- 🧠 Caption: a woman holding a phone near a computer


## Model Used
- Component	Name / Framework
- Captioning Model	Salesforce/blip-image-captioning-base
- Framework	Hugging Face Transformers
- Backend	PyTorch

## 💡 Future Improvements

- 🧩 Add YOLO object detection for region-focused captions

- 🧠 Integrate OAK-D Light for depth and 3D perception

- 🔊 Combine with speech synthesis for a talking assistant robot

# 👩‍💻 Author

## Sabera Banu
### Department of Computer Science & Engineering
### Sejong University, South Korea