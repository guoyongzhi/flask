#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import datetime
import time
tim = datetime.datetime.now()
a_time = datetime.datetime.strptime("2021-01-13 15:18:30", "%Y-%m-%d %H:%M:%S")
print(a_time)
print(type(a_time))
lo_time = (tim - a_time).total_seconds()
print(lo_time)
if lo_time < 5 * 60:
    print(True)
else:
    print(False)