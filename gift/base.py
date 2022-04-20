# coding:utf-8

'''
1: 导入user.json 文件检查
2: 导入gift.json 文件检查
'''


'''
1: 确定用户表中每个用户的信息字端
2：读取userjson文件
3：写入userjson文件（检测该用户是否存在），存在则不可写入

username 姓名
role normal or admin
active True or False
create_time timestamp
update_time timestamp
gifts [] 
'''
import os
import json
import time
from common.utils import check_file
from common.error import UserExistsError
from common.utils import timestamp_to_string


class Base(object):
    def __init__(self, user_json, gift_json):
        self.user_json = user_json
        self.gift_json = gift_json

        self.__check_user_json()
        self.__check_gift_json()

    def __check_user_json(self):
        check_file(self.user_json)

    def __check_gift_json(self):
        check_file(self.gift_json)

    def __read_users(self, time_to_str=False):
        with open(self.user_json, 'r') as f:
            data = json.loads(f.read())

        if time_to_str == True:
            for username, v in data.items():
                v['create_time'] = timestamp_to_string(v['create_time'])
                v['update_time'] = timestamp_to_string(v['update_time'])
                data[username] = v

        return data

    def __write_user(self, **user):
        if 'username' not in user:
            raise ValueError('missing username')
        if 'role' not in user:
            raise ValueError('missing role')

        user['active'] = True
        user['create_time'] = time.time()
        user['update_time'] = time.time()
        user['gifts'] = []

        users = self.__read_users()
        if user['username'] in users:
            raise UserExistsError('username %s had exists' % user['username'])

        users.update(
            {user['username']: user}
        )

        json_users = json.dumps(users)

        with open(self.user_json, 'w') as f:
            f.write(json_users)



if __name__ == '__main__':
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    base = Base(user_path, gift_path)
    base.write_user(username='dewei', role='admin')


