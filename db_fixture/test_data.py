import random
import sys
import time

sys.path.append('../db_fixture')
try:
    from mysql_db import DB
except ImportError:
    from .mysql_db import DB

# 定义过去时间
past_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 100000))

# 定义将来时间
future_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 10000))

# 定义id
randomNum = random.randint(0, 1000)
randomNum2 = random.randint(0, 1000)
# create data
datas = {
    'sign_event': [
        {'id': randomNum+1, 'name': '红米Pro发布会', '`limit`': 2000, 'status': 1, 'address': '北京会展中心',
         'start_time': future_time, 'create_time': past_time},
        {'id': randomNum+2, 'name': '可参加人数为0', '`limit`': 0, 'status': 1, 'address': '北京会展中心',
         'start_time': future_time, 'create_time': past_time},
        {'id': randomNum+3, 'name': '当前状态为0关闭', '`limit`': 2000, 'status': 0, 'address': '北京会展中心',
         'start_time': future_time, 'create_time': past_time},
        {'id': randomNum+4, 'name': '发布会已结束', '`limit`': 2000, 'status': 1, 'address': '北京会展中心',
         'start_time': past_time, 'create_time': past_time},
        {'id': randomNum+5, 'name': '小米5发布会', '`limit`': 2000, 'status': 1, 'address': '北京国家会议中心',
         'start_time': future_time, 'create_time': past_time},
    ],
    'sign_guest': [
        {'id': randomNum2+1, 'name': 'alen', 'phone': 13511001100, 'email': 'alen@mail.com', 'sign': 0,
         'event_id': randomNum+1, 'create_time': past_time},
        {'id': randomNum2+2, 'name': 'has sign', 'phone': 13511001101, 'email': 'sign@mail.com', 'sign': 1,
         'event_id': randomNum+2, 'create_time': past_time},
        {'id': randomNum2+3, 'name': 'tom', 'phone': 13511001102, 'email': 'tom@mail.com', 'sign': 0,
         'event_id': randomNum+3, 'create_time': past_time},
    ],
}


# Inster table datas
def init_data():
    DB().init_data(datas)


if __name__ == '__main__':
    init_data()
