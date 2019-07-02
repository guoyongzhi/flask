from flask import Flask, request
from geventwebsocket.websocket import WebSocket
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from uuid import uuid4

# from baidu_asr_and_synthesis import new_asr, new_synthesis
# from simple_questions_answers import question_answer

app = Flask(__name__)  # type:Flask


@app.route('/ws')
def ws():
    user_websocket = request.environ.get('wsgi.websocket')  # type:WebSocket
    if user_websocket:
        while 1:
            res = user_websocket.receive()
            # 保存接收音频文件
            rev_file_name = ("%s" + ".wav") % str(uuid4())
            with open(rev_file_name, 'wb') as f:
                f.write(res)
            print(rev_file_name)
            # 将接收的音频文件转换为文本
            audio_to_text = new_asr(rev_file_name)
            print('audio_to_text', audio_to_text)
            # 根据问题文本回答问题
            answer_text = question_answer(audio_to_text)
            print('answer_text',answer_text)
            # 将问题答案转成音频文件
            answer_audio_file_path = new_synthesis(answer_text)
            print('answer_audio_file_path',answer_audio_file_path)
            # 将音频文件路径发给前端
            user_websocket.send(answer_audio_file_path)


if __name__ == '__main__':
    http_serv = WSGIServer(('127.0.0.1', 9528), app, handler_class=WebSocketHandler)
    http_serv.serve_forever()
