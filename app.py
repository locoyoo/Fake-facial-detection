from flask import Flask,render_template,request,jsonify
from flask_dropzone import Dropzone
import os,base64
import numpy as np
from PIL import Image
# import filetype
from static.algorithm.backend import receiveInput
import time
app = Flask(__name__)
dropzone=Dropzone(app)
basedir = os.path.abspath(os.path.dirname(__file__))
judge=False
app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'upload'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM=True,
    DROPZONE_ALLOWED_FILE_TYPE='image/*,.mp4',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=10,
    # DROPZONE_IN_FORM=True,
    DROPZONE_UPLOAD_ON_CLICK=True,
    # DROPZONE_UPLOAD_ACTION='upload',  # URL or endpoint
    # DROPZONE_UPLOAD_BTN_ID='upload'
)

@app.route('/')
def home():
    return render_template("Demo.html")
@app.route('/predict',methods=['POST','GET'])
def predict():
    result1 = {
        "static/images/testResult1.jpg": True,
    }
    files=[]
    files_bool=[]
    root=app.config['UPLOADED_PATH']
    print(request.data)
    result={}
    print(len(request.data.decode()))
    data_get=request.data.decode().split(',')#数组，存储发过来的值
    for i in range(0,len(data_get)-1):
        if(data_get[i].split('.')[1]=='mp4'):
            files_bool.append(True)
        else:
            files_bool.append(False)
        files.append(data_get[i])
    # for file in request.data.decode().split(","):
    #     print(file.split('.'))
    #     if (file.split('.')[1] == 'mp4'):
    #         files_bool.append(True)
    #     else:
    #         files_bool.append(False)
    #     files.append(file)

    # print(files)
    # print(files_bool)
    # print(root)
    result = receiveInput(root, files_bool, files, int(data_get[len(data_get)-1]))
    return result

@app.route('/upload', methods=['POST','GET'])
def upload():
    result1={
        "static/images/testResult1.jpg":True,
        "static/images/testResult2.jpg":False
    }
    # judge=False
    root=app.config['UPLOADED_PATH']
    files=[]
    files_bool=[]
    file_paths=[]
    data={}
    if request.method == 'POST':
            # for file in request.data.decode().split(","):
            #     print(file.split('.'))
            #     if (file.split('.')[1] == 'mp4'):
            #         files_bool.append(True)
            #     else:
            #         files_bool.append(False)
            #     files.append(file)

            for key, f in request.files.items():
                if key.startswith('file'):
                    f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))#存储已经上传的图片和视频
                    files.append(f.filename)
                    if(f.filename.split('.')[1]=='mp4'):
                        files_bool.append(True)
                    else:
                        files_bool.append(False)
    print(files)
    print(files_bool)
    print(root)
                # return jsonify(f.filename)

    # print(result)
    # for index in range(0,len(files)):
    #     file_path.append(root+"\\"+files[index])
    # for index in range(0,len(files)):
    #     data[file_path[index]]=float(result[index])
    # print(data)
    # result = receiveInput(root, files_bool, files)
    # print(result)
    return render_template('Demo.html')
# 需要返回

if __name__ == '__main__':
    app.run()
