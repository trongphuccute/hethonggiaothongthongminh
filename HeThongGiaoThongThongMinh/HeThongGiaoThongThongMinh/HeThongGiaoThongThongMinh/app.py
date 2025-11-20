from flask import Flask, render_template, request, Response, url_for, jsonify
from ultralytics import YOLO
import os
import shutil
import cv2

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
RESULT_FOLDER = os.path.join(basedir, 'static', 'results')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Đường dẫn model
model = YOLO(r"C:\hethonggiaothongthongminh\HeThongGiaoThongThongMinh\HeThongGiaoThongThongMinh\HeThongGiaoThongThongMinh\HeThongGiaoThongThongMinh-feature-YoloIntegration\runs\detect\train3\weights\best.pt")

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nhandien')
def nhandien():
    return render_template('nhandien.html', uploaded_image=None, uploaded_video=None, original_filename=None)

# Các route tĩnh khác giữ nguyên
@app.route('/bienbaocam')
def bienbaocam():
    return render_template('bienbaocam.html')

@app.route('/bbnguyhiem')
def bbnguyhiem():
    return render_template('bbnguyhiem.html')

@app.route('/bbhieulenh')
def bbhieulenh():
    return render_template('bbhieulenh.html')

@app.route('/bbchidan')
def bbchidan():
    return render_template('bbchidan.html')

@app.route('/vkd')
def vkd():
    return render_template('vkd.html')

@app.route('/quizz')
def quizz():
    return render_template('quizz.html')

@app.route('/quizz2')
def quizz2():
    return render_template('quizz2.html')

@app.route('/quizz3')
def quizz3():
    return render_template('quizz3.html')

@app.route('/quizz4')
def quizz4():
    return render_template('quizz4.html')

@app.route('/dieuluat')
def dieuluat():
    return render_template('dieuluat.html')

@app.route('/mucphat')
def mucphat():
    return render_template('mucphat.html')

@app.route('/lichsu')
def lichsu():
    return render_template('lichsu.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "❌ Không có file tải lên", 400

    file = request.files['image']
    if file.filename == '':
        return "❌ File không hợp lệ", 400

    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    if ext in ['.mp4', '.avi', '.mov', '.mkv']:
        # Khi upload video, trả về trang gọi streaming video xử lý từng frame
        return render_template('nhandien.html', uploaded_video=None, original_filename=filename, uploaded_image=None, stream_video_url=url_for('process_video_feed', file=filename))

    else:
        results = model.predict(source=input_path, conf=0.25, save=True, project='runs/detect', name='web_detect')

        result_dir = results[0].save_dir
        detected_image = None
        for f in os.listdir(result_dir):
            if f.lower().endswith(('.jpg', '.png')):
                detected_image = os.path.join(result_dir, f)
                break

        if not detected_image:
            return "❌ Không tìm thấy ảnh kết quả", 500

        output_filename = os.path.basename(detected_image)
        final_path = os.path.join(RESULT_FOLDER, output_filename)
        shutil.copy(detected_image, final_path)

        return render_template('nhandien.html', uploaded_image=url_for('static', filename=f'results/{output_filename}'), original_filename=filename, uploaded_video=None, stream_video_url=None)


@app.route('/upload_api', methods=['POST'])
def upload_api():
    if 'image' not in request.files:
        return jsonify({'error': 'Không có file tải lên'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'File không hợp lệ'}), 400

    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    if ext in ['.mp4', '.avi', '.mov', '.mkv']:
        video_url = url_for('process_video_feed', file=filename)
        return jsonify({'stream_video_url': video_url})

    else:
        results = model.predict(source=input_path, conf=0.25, save=True, project='runs/detect', name='web_detect')

        result_dir = results[0].save_dir
        detected_image = None
        for f in os.listdir(result_dir):
            if f.lower().endswith(('.jpg', '.png')):
                detected_image = os.path.join(result_dir, f)
                break

        if not detected_image:
            return jsonify({'error': 'Không tìm thấy ảnh kết quả'}), 500

        output_filename = os.path.basename(detected_image)
        final_path = os.path.join(RESULT_FOLDER, output_filename)
        shutil.copy(detected_image, final_path)

        image_url = url_for('static', filename=f'results/{output_filename}')
        return jsonify({'uploaded_image': image_url})


# Hàm stream video xử lý từng frame theo thời gian thực
@app.route('/process_video_feed')
def process_video_feed():
    filename = request.args.get('file')
    if not filename:
        return "Thiếu tham số file", 400

    video_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(video_path):
        return "File không tồn tại", 404

    cap = cv2.VideoCapture(video_path)

    def generate():
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Dự đoán trên từng frame
            results = model.predict(source=frame, conf=0.4, save=False)
            annotated_frame = results[0].plot()

            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        cap.release()

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Stream webcam (giữ nguyên)
def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        results = model.predict(source=frame, conf=0.4, save=False)
        annotated_frame = results[0].plot()
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
