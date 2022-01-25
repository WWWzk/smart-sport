from flask import Flask, render_template, request, flash, redirect, url_for, make_response, jsonify
from flask_bootstrap import Bootstrap
import base64
import os
import time
import json

from main import match
from werkzeug.utils import secure_filename

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(24)

basedir = os.path.abspath(os.path.dirname(__file__))
uploadDir = os.path.join(basedir, 'static/uploads')


@app.route('/', methods=['POST', 'GET'])
def process():
    if request.method == 'POST':
        #print("request",request)
        #print(request.form)
        video_id = request.form.get('video_id')
        #得到文件路径
        filename=request.form.get('video')
        #获取检测的动作类型
        #返回一个数字字符
        #1表示抱膝提踵
        #2表示原地弓步跳
        #3表示侧向台阶跳
        action_type=request.form.get('action_type')

        function_type = request.form.get('function_type')
        #限时时间，可以不填写，就为空,字符串类型
        time_limit=request.form.get('time_limit')
        if(action_type=='0'):
            flash('请选择动作', 'danger');
            return render_template('base.html');

        uploadDir=os.getcwd()+"/static/uploads/"

        print("filename",filename)
        print("selectType",action_type)
        print("limitTime",time_limit)
        time_limit = float(time_limit) if time_limit != '' else None
        print("limitTime", time_limit)
        rst, reason = match(action_type + '.mp4', uploadDir + filename, time_limit=time_limit)

        #根据filename文件名得到相应的结果
        # 相似度
        similarity = ""
        # 计数结果
        counting_result = ""
        if action_type == 'identification_1':
            similarity = rst
        else:
            counting_result = rst
        # 最高分
        highest_score = str(reason['max_score']) if reason and 'max_score' in reason else 'null'
        # 最低分
        lowest_score = str(reason['min_score']) if reason and 'max_score' in reason else 'null'

        #json字符串
        jsonString=json.dumps(reason) if reason else '{}'
        #限时时间


        #待实现内容
        #
        #
        # time.sleep(10)
        #
        ################

        types = ['mp4', 'avi', 'mkv','flv','dat']
        if filename.split('.')[-1] in types:
            uploadpath = os.path.join(uploadDir, filename)
            print(uploadpath)
            flash('检测成功', 'success')
            return render_template('base.html', show_wait="", videoname=filename, similarity=similarity,
                                   counting_result=counting_result)
            # return render_template('base.html', show_wait="",videoname=filename,similarity=similarity,highest_score=highest_score,
            #                        lowest_score=lowest_score,counting_result=counting_result,jsonString=jsonString)
        else:
            flash('检测失败', 'danger')


    return render_template('base.html')


@app.route('/process', methods=['POST'])
def action_match():
    ret_info = {
        'video_id': '',
        'score': '',
        'count': '',
        'err_msg': ''
    }
    params = request.get_json()

    basepath = os.path.dirname(__file__)
    action_type = params.get('action_type')
    function_type = params.get('function_type')
    video_id = params.get('video_id')
    time_limit = params.get('time_limit')
    if not video_id or not action_type or not function_type:
        ret_info['err_msg'] = 'missing parameters'
        return ret_info
    ret_info['video_id'] = video_id
    current_time = time.localtime(time.time())
    dir_path = os.path.join(basepath, 'data/%d-%d-%d'%current_time[:3])
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    video_name = '%s-%s-%s-%s.mp4' % (video_id, action_type, function_type, time_limit)
    video_path = os.path.join(dir_path, video_name)
    video = params.get('video')
    print(type(video))
    video = base64.b64decode(video.encode('ascii'))

    with open(video_path, 'wb') as f:
        f.write(video)


    time_limit = float(time_limit) if time_limit != '' else None
    # print(action_type, video_path)
    rst, reason = match(action_type, video_path, time_limit=time_limit)
    rst = str(rst)
    if function_type == '0':
        ret_info['score'] = rst
    else:
        ret_info['count'] = rst
    return make_response(jsonify(ret_info))


if __name__ == '__main__':
    app.run(debug=True)

