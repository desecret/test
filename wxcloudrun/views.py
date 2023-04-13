from flask import Flask, request, jsonify
import requests
from aip import AipFace
import base64

# 配置百度AI的API Key和Secret Key
APP_ID = '32029639'
API_KEY = 'kwwW6n7OihkDPNU9cGG8QDpw'
SECRET_KEY = 'y3eDQM53Sd9mPiRtz7HoWTpAjBarIWT9'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)


app = Flask(__name__)


#登录
@app.route('/login', methods=['POST'])
def login():
    # 获取微信小程序登录凭证code
    code = request.json['code']

    # 调用微信API获取用户唯一标识openid和会话密钥session_key
    app_id = 'wx2916ac9174b5b651'
    app_secret = '5f290d5dc4420107b941806b585b7424'
    wx_api_url = f'https://api.weixin.qq.com/sns/jscode2session?appid={app_id}&secret={app_secret}&js_code={code}&grant_type=authorization_code'
    response = requests.get(wx_api_url)
    wx_data = response.json()

    # 返回用户唯一标识openid和会话密钥session_key给前端
    return jsonify(wx_data)

'''
#上传图片视频
@app.route('/upload', methods=['POST'])
def upload():
    # 获取前端上传的文件
    file = request.files['file']

    # 将文件转换成Base64编码格式
    file_content = base64.b64encode(file.read()).decode('utf-8')

    # 将Base64编码格式的文件发送给微信云托管
    cloud_api_url = 'https://api.weixin.qq.com/tcb/uploadfile?access_token=ACCESS_TOKEN'
    access_token = 'your_access_token'
    cloud_api_url = cloud_api_url.replace('ACCESS_TOKEN', access_token)
    headers = {'content-type': 'application/json'}
    data = {
        'env': 'prod-9gqfxhub4c1b0ff6',
        'path': 'your_path',
        'file': file_content
    }
    response = requests.post(cloud_api_url, headers=headers, json=data)
    cloud_data = response.json()

    # 将文件ID发送给后端服务器
    file_id = cloud_data['file_id']

    # 返回文件ID给前端
    return jsonify({'file_id': file_id})

'''
#人脸识别
@app.route('/face', methods=['POST'])
def face():
    # 获取前端上传的图片ID
    file_id = request.json['file_id']

    # 从微信云托管下载图片
    cloud_api_url = 'https://api.weixin.qq.com/tcb/batchdownloadfile?access_token=ACCESS_TOKEN'
    access_token = '67_3mkvr2YQ0S6_evE56xi7sxmujftM5DrzczOXvh5FPGoOs_Lx8-GTIsB13CLwNC8iTipwOFZLA9pW8rNVmFvVJZF62t4IwxlN0bKS8gTkZb6SHusOz0JVQzZ3ZH4CAZeACAJHG'
    cloud_api_url = cloud_api_url.replace('ACCESS_TOKEN', access_token)
    headers = {'content-type': 'application/json'}
    data = {
        'env': 'test-2grzno7eef45aae3',
        'file_list': [{'fileid': file_id
    }]
    }
    response = requests.post(cloud_api_url, headers=headers, json=data)
    cloud_data = response.json()

    # 获取下载后的图片内容并进行Base64编码
    image_content = base64.b64encode(cloud_data['file_list'][0]['download_url'].content).decode('utf-8')

    # 调用百度AI的人脸检测API获取人脸信息
    image_type = 'BASE64'
    options = {'face_field': 'age,gender,beauty,expression'}
    result = client.detect(image_content, image_type, options)

    # 返回人脸信息给前端
    return jsonify(result)


#视频活体检测
@app.route('/livetest', methods=['POST'])
def livetest():
    # 获取前端上传的视频ID
    file_id = request.json['file_id']

    # 从微信云托管下载视频
    cloud_api_url = 'https://api.weixin.qq.com/tcb/batchdownloadfile?access_token=ACCESS_TOKEN'
    access_token = '67_3mkvr2YQ0S6_evE56xi7sxmujftM5DrzczOXvh5FPGoOs_Lx8-GTIsB13CLwNC8iTipwOFZLA9pW8rNVmFvVJZF62t4IwxlN0bKS8gTkZb6SHusOz0JVQzZ3ZH4CAZeACAJHG'
    cloud_api_url = cloud_api_url.replace('ACCESS_TOKEN', access_token)
    headers = {'content-type': 'application/json'}
    data = {
        'env': 'test-2grzno7eef45aae3',
        'file_list': [{'fileid': file_id}]
    }
    response = requests.post(cloud_api_url, headers=headers, json=data)
    cloud_data = response.json()

    # 获取下载后的视频内容并进行Base64编码
    video_content = base64.b64encode(cloud_data['file_list'][0]['download_url'].content).decode('utf-8')

    # 调用百度AI的视频活体检测API进行活体检测
    options = {'liveness_control': 'HIGH'}
    result = client.videoFaceliveness(video_content, options)

    # 返回活体检测结果给前端
    return jsonify(result)


#人脸注册
@app.route('/faceregister', methods=['POST'])
def faceregister():
    # 获取前端上传的图片ID和用户ID
    file_id = request.json['file_id']
    user_id = request.json['user_id']

    # 从微信云托管下载图片
    cloud_api_url = 'https://api.weixin.qq.com/tcb/batchdownloadfile?access_token=ACCESS_TOKEN'
    access_token = '67_3mkvr2YQ0S6_evE56xi7sxmujftM5DrzczOXvh5FPGoOs_Lx8-GTIsB13CLwNC8iTipwOFZLA9pW8rNVmFvVJZF62t4IwxlN0bKS8gTkZb6SHusOz0JVQzZ3ZH4CAZeACAJHG'
    cloud_api_url = cloud_api_url.replace('ACCESS_TOKEN', access_token)
    headers = {'content-type': 'application/json'}
    data = {
        'env': 'test-2grzno7eef45aae3',
        'file_list': [{'fileid': file_id}]
    }
    response = requests.post(cloud_api_url, headers=headers, json=data)
    cloud_data = response.json()

    # 获取下载后的图片内容并进行Base64编码
    image_content = base64.b64encode(cloud_data['file_list'][0]['download_url'].content).decode('utf-8')

    # 调用百度AI的人脸注册API进行人脸注册
    image_type = 'BASE64'
    group_id = 'group1'
    result = client.addUser(image_content, image_type, group_id, user_id)

    # 返回人脸注册结果给前端
    return jsonify(result)


#人脸搜索
@app.route('/facesearch', methods=['POST'])
def facesearch():
    # 获取前端上传的图片ID
    file_id = request.json['file_id']

    # 从微信云托管下载图片
    cloud_api_url = 'https://api.weixin.qq.com/tcb/batchdownloadfile?access_token=ACCESS_TOKEN'
    access_token = '67_3mkvr2YQ0S6_evE56xi7sxmujftM5DrzczOXvh5FPGoOs_Lx8-GTIsB13CLwNC8iTipwOFZLA9pW8rNVmFvVJZF62t4IwxlN0bKS8gTkZb6SHusOz0JVQzZ3ZH4CAZeACAJHG'
    cloud_api_url = cloud_api_url.replace('ACCESS_TOKEN', access_token)
    headers = {'content-type': 'application/json'}
    data = {
        'env': 'test-2grzno7eef45aae3',
        'file_list': [{'fileid': file_id}]
    }
    response = requests.post(cloud_api_url, headers=headers, json=data)
    cloud_data = response.json()

    # 获取下载后的图片内容并进行Base64编码
    image_content = base64.b64encode(cloud_data['file_list'][0]['download_url'].content).decode('utf-8')

    # 调用百度AI的人脸搜索API进行人脸搜索
    image_type = 'BASE64'
    group_id = 'group1'
    result = client.search(image_content, image_type, group_id)

    # 返回人脸搜索结果给前端
    return jsonify(result)
