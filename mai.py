from app import app
from gevent import monkey
from geventwebsocket.server import WSGIServer
from geventwebsocket.handler import WebSocketHandler


monkey.patch_all()
    

if __name__ == '__main__':
    http_server = WSGIServer(('192.168.11.103', 8081), app, handler_class=WebSocketHandler)
    http_server.serve_forever()

