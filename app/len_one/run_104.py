from app.len_one.smin_send_car import *

a = 0
while a < 500:
    def_log = logger.logs("四哥很帅")
    open_gae(host="192.168.11.104", cl="192.168.1.170", car="豫C813RG", openSendCar=def_log)
    time.sleep(random.randint(30, 120))
    open_gae(host="192.168.11.104", cl="192.168.1.175", car="豫C813RG", openSendCar=def_log)
    time.sleep(random.randint(30, 120))
    a += 1
