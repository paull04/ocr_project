from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import easyocr

reader = easyocr.Reader(['ko', 'en'], gpu=False)


app = Flask(__name__)

# 업로드 HTML 렌더링
@app.route('/')
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