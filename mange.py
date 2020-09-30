
from flask import Flask, request
# from geventwebsocket.websocket import WebSocket
from flask_socketio import SocketIO, send, emit, leave_room
from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from uuid import uuid4

# from baidu_asr_and_synthesis import new_asr, new_synthesis
# from simple_questions_answers import question_answer
# from static.aip.new_asr import *

monkey.patch_all()
app = Flask(__name__)  # type:
# socketio = SocketIO(app)


@app.route('/ws')
def ws():
    ws = request.environ.get('wsgi.websocket')  # type:
    if ws:
        ws = request.environ['wsgi.websocket']
        while 1:
            try:
                res = ws.receive()
                print(res)
            except Exception:
                print(e)
            # 保存接收音频文件
            # rev_file_name = ("%s" + ".wav") % str(uuid4())
            # with open(rev_file_name, 'wb') as f:
            #     f.write(res)
            # print(rev_file_name)
            # # 将接收的音频文件转换为文本
            # audio_to_text = new_asr(rev_file_name)
            # print('audio_to_text', audio_to_text)
            # # 根据问题文本回答问题
            # answer_text = question_answer(audio_to_text)
            # print('answer_text',answer_text)
            # # 将问题答案转成音频文件
            # answer_audio_file_path = new_synthesis(answer_text)
            # print('answer_audio_file_path',answer_audio_file_path)
            # # 将音频文件路径发给前端
            try:
                ws.send(res)
            except Exception as e:
                if 'Socket is dead' in str(e):
                    print("找到了")
                    break
    return "OK"


# @socketio.on('message')
def send_message(message):
    send(message)
    

# @socketio.on('my event')
def emit_message(message):
    emit("say", message, broadcast=True)


# @socketio.on('leave')
def leave(message):
    room = message['room']
    leave_room(room)
    send(room + '离开', room=room)


if __name__ == '__main__':
    http_serv = WSGIServer(('192.168.11.103', 8081), app, handler_class=WebSocketHandler)
    http_serv.serve_forever()
