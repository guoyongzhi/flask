import unittest
import requests
from datetime import *
from axf.dbmysql import *
import random
import parameterized


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)
    
    @staticmethod
    @parameterized.parameterized.expand(my_db_select('', ''))
    def test_setWarningRecord():
        url = 'http://192.168.11.156:8012/SenseWarning/Index'
        headers = {"Content-Type": "application/json"}
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        temp = random.uniform(35.0, 45.0)
        if temp > 37.3:
            temp_status = 2
        else:
            temp_status = 1
        face_attr = {"respirator_color": "color_type_other"}
        data = dict(face_attr=face_attr, device_id="魔力豪", channel=3, lib_id=3, lib_name="白名单", lib_type=2, snap_age=23,
                    snap_gender=1, snap_path="snap_pic", img_path="img_pic", img_id="65568", ip="192.168.11.133",
                    trigger=now, person_name="娄松亚_000000000000000000_1", temp=temp, temp_unit=0,
                    temp_status=temp_status, similarity=90, obj_label=1)
        date = {"json": data, "msg_id": 774}
        res = requests.post(url=url, data=date, headers=headers)
        print(res.text)


if __name__ == '__main__':
    unittest.main()
