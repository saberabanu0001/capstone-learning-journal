import cv2
import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration
from PIL import Image
import depthai as dai

# -----------------------------
# CONFIGURATION
# -----------------------------
USE_OAKD = True  # ✅ Set to True for OptiCamera (OAK-D), False for MacBook webcam
# Using locally downloaded LLaVA 1.5 7B model for better accuracy than BLIP
MODEL_PATH = "/Users/saberabanu/llava-1.5-7b-hf"

# -----------------------------
# LOAD THE VISION-LANGUAGE MODEL
# -----------------------------
print("🧠 Loading LLaVA Vision-Language Model from local path...")
processor = AutoProcessor.from_pretrained(MODEL_PATH, local_files_only=True)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = LlavaForConditionalGeneration.from_pretrained(
    MODEL_PATH,
    dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto" if torch.cuda.is_available() else None,
    low_cpu_mem_usage=True,
    local_files_only=True
)
if device == "cpu":
    model.to(device)
print("✅ LLaVA model loaded successfully on", device.upper())

# -----------------------------
# SETUP CAMERA (OAK-D OR WEBCAM)
# -----------------------------
if USE_OAKD:
    # OAK-D pipeline setup
    pipeline = dai.Pipeline()
    cam_rgb = pipeline.create(dai.node.ColorCamera)
    cam_rgb.setPreviewSize(640, 480)
    cam_rgb.setInterleaved(False)
    xout_rgb = pipeline.create(dai.node.XLinkOut)
    xout_rgb.setStreamName("rgb")
    cam_rgb.preview.link(xout_rgb.input)
    device_oak = dai.Device(pipeline)
    q_rgb = device_oak.getOutputQueue(name="rgb", maxSize=1, blocking=False)
    print("🎥 OAK-D Camera connected.")
else:
    cap = cv2.VideoCapture(0)
    print("🎥 MacBook webcam connected.")

# -----------------------------
# MAIN LOOP
# -----------------------------
print("\n🚀 LLaVA Vision-Language Live Captioning Started (press 'q' to quit)")
frame_count = 0
last_caption = ""

while True:
    # Capture frame from camera
    if USE_OAKD:
        in_rgb = q_rgb.tryGet()
        if in_rgb is None:
            continue
        frame = in_rgb.getCvFrame()
    else:
        ret, frame = cap.read()
        if not ret:
            break

    frame_count += 1

    # Process one frame every 90 frames (~3 seconds) - LLaVA is slower than BLIP
    if frame_count % 90 == 0:
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # LLaVA requires a conversation-style prompt (note: <image> token is handled by processor)
        prompt = "USER: <image>\nDescribe what you see in this image in one clear sentence. ASSISTANT:"
        
        # Process inputs - explicitly pass text and image to avoid ambiguity
        inputs = processor(text=prompt, images=img, return_tensors="pt")
        inputs = {key: value.to(device) for key, value in inputs.items()}

        # Generate caption
        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=50, do_sample=False)
        
        # Decode the response
        caption = processor.decode(output[0], skip_special_tokens=True)
        # Extract only the assistant's response (remove the prompt)
        if "ASSISTANT:" in caption:
            caption = caption.split("ASSISTANT:")[-1].strip()
        
        last_caption = caption
        print(f"🧠 LLaVA: {caption}")

        # Display caption on screen
        # Split long captions into multiple lines for better display
        y_offset = 40
        words = caption.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if len(test_line) > 50:  # Max characters per line
                if current_line:
                    lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)
        
        for i, line in enumerate(lines[:3]):  # Show max 3 lines
            cv2.putText(frame, line, (20, y_offset + i * 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    elif last_caption:
        # Show last caption while processing
        words = last_caption.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if len(test_line) > 50:
                if current_line:
                    lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)
        
        y_offset = 40
        for i, line in enumerate(lines[:3]):
            cv2.putText(frame, line, (20, y_offset + i * 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("LLaVA VLM Camera Captioning", frame)

    # Quit when 'q' pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -----------------------------
# CLEANUP
# -----------------------------
if not USE_OAKD:
    cap.release()
cv2.destroyAllWindows()
print("🛑 Stream stopped successfully.")

