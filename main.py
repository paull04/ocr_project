from flask import Flask, render_template, request, Response, stream_with_context
from werkzeug.utils import secure_filename
import cv2
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import easyocr
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

reader = easyocr.Reader(['ko', 'en'], gpu=False)

app = Flask(__name__)
def streaming():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            return
        res = model(frame).render()
        ret, buffer = cv2.imencode('.jpg', res[0])
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video')
def video():
    return Response(streaming(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def video_show():
    return render_template('streaming.html')
# 업로드 HTML 렌더링
@app.route('/upload')
def render_file():
    return render_template('upload.html')

# 파일 업로드 처리
@app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # 저장할 경로 + 파일명
        f.save(secure_filename(f.filename))
        img_path = f.filename
        ret = ''
        for x in reader.readtext(img_path):
            ret = x[1] +'\n'
        return ret





if __name__ == '__main__':
    # 서버 실행
    app.run(debug = True)