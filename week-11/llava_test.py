import cv2
import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration
from PIL import Image
import depthai as dai
import os

# -----------------------------
# CONFIGURATION
# -----------------------------
USE_OAKD = True  # ✅ Set to True for OptiCamera (OAK-D), False for MacBook webcam
HEADLESS = True  # ✅ Set to True to disable OpenCV display windows (useful over SSH)
SYSTEM_PROMPT = os.environ.get(
    "LLAVA_SYSTEM_PROMPT",
    "You are an assistant that watches the robot's live camera feed and describes what you see in one or two concise sentences.",
)
MODEL_PATH = os.environ.get("LLAVA_MODEL_PATH", "/Users/saberabanu/llava-1.5-7b-hf")
MAX_NEW_TOKENS = int(os.environ.get("LLAVA_MAX_NEW_TOKENS", "80"))

if HEADLESS:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    print("🙈 Headless mode enabled: suppressing OpenCV display windows.")

# -----------------------------
# LOAD THE VISION-LANGUAGE MODEL
# -----------------------------
print("🧠 Loading LLaVA Vision-Language Model from local path...")
processor = AutoProcessor.from_pretrained(
    MODEL_PATH,
    local_files_only=True,
    trust_remote_code=True,
)

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

model = LlavaForConditionalGeneration.from_pretrained(
    MODEL_PATH,
    torch_dtype=dtype,
    low_cpu_mem_usage=True,
    local_files_only=True,
    trust_remote_code=True,
)
if device == "cpu":
    model.to(device)
model.eval()
print("✅ Model loaded successfully on", device.upper())

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
print("\n🚀 Vision-Language Live Captioning Started (press 'q' to quit)")
frame_count = 0

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

    # Process one frame every 60 frames (~2 seconds)
    if frame_count % 60 == 0:
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        conversation = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [{"type": "image"}],
            },
        ]
        prompt = processor.apply_chat_template(
            conversation, add_generation_prompt=True, tokenize=False
        )
        inputs = processor(
            text=prompt,
            images=img,
            return_tensors="pt",
        ).to(device)

        with torch.inference_mode():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=False,
                eos_token_id=model.config.eos_token_id,
            )

        decoded = processor.batch_decode(output_ids, skip_special_tokens=True)[0]
        caption = decoded.split("ASSISTANT:")[-1].strip()
        print(f"🧠 {caption}")

        if not HEADLESS:
            # Display caption on screen
            cv2.putText(
                frame,
                caption,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                2,
            )

    if not HEADLESS:
        cv2.imshow("VLM Camera Captioning", frame)

        # Quit when 'q' pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# -----------------------------
# CLEANUP
# -----------------------------
if not USE_OAKD:
    cap.release()
if not HEADLESS:
    cv2.destroyAllWindows()
print("🛑 Stream stopped successfully.")
