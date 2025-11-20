import sys, os, cv2, numpy as np
from ultralytics import YOLO
from PIL import ImageFont, ImageDraw, Image

sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
from distance_estimation import estimate_distance
from sign_analysis import analyze_sign
from log_manager import log_event, alert_user

# Hàm vẽ text Unicode
def draw_text_unicode(img, text, pos, font_size=24, color=(0,255,0)):
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype("arial.ttf", font_size)
    draw.text(pos, text, font=font, fill=color)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

# Hàm crop & zoom vùng trung tâm (giả định biển báo thường ở giữa khung hình)
def crop_and_zoom(frame, zoom_factor=1.5):
    h, w = frame.shape[:2]
    new_w, new_h = int(w/zoom_factor), int(h/zoom_factor)
    x1, y1 = (w - new_w)//2, (h - new_h)//2
    x2, y2 = x1 + new_w, y1 + new_h
    cropped = frame[y1:y2, x1:x2]
    return cv2.resize(cropped, (w, h))

# Load model
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
model_path = os.path.join(project_root, "runs", "detect", "train3", "weights", "best.pt")
print("🔎 Model:", model_path)
model = YOLO(model_path)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Không mở được webcam.")
    sys.exit()

print("🚦 Hệ thống nhận dạng biển báo giao thông đang chạy...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Crop & zoom để tăng khả năng nhận dạng xa
    frame_zoomed = crop_and_zoom(frame, zoom_factor=1.5)

    results = model.predict(source=frame_zoomed, stream=True, conf=0.25)

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            distance = estimate_distance(x1, y1, x2, y2)
            info = analyze_sign(cls)
            name = info.get("name", f"Class {cls}")
            advice = info.get("advice", "")

            alert_msg = f"{name} ({distance}m) - {advice}"
            alert_user(alert_msg)
            log_event(f"{name}, distance={distance}m, conf={conf:.2f}")

            color = (0,255,0) if info.get("type") != "Cấm" else (0,0,255)
            cv2.rectangle(frame_zoomed, (x1,y1), (x2,y2), color, 2)
            frame_zoomed = draw_text_unicode(frame_zoomed, f"{name} {distance}m", (x1, y1-25), 24, color)

    cv2.imshow("Smart Traffic System (Realtime)", frame_zoomed)

    if cv2.waitKey(1) & 0xFF in [ord('q'), 27]:
        print("🛑 Đang tắt hệ thống...")
        break

cap.release()
cv2.destroyAllWindows()
print("✅ Đã dừng hệ thống.")