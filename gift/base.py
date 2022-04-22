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
'''

1: role 修改
2: active 修改
3: delete_user

'''
'''
1: gifts 奖品结构的确定
2：gifts 奖品的读取
3：gifts 添加
4：gifts 初始化
{
    level1: { 
        level1: { gift_name: { name: xx, count: xx}}, 
        level2: {}, 
        level3: {} 
    },
    level2: { 
        level1: { gift_name: { name: xx, count: xx}}, 
        level2: {}, 
        level3: {} 
    },
    level3: { 
        level1: { gift_name: { name: xx, count: xx}}, 
        level2: {}, 
        level3: {} 
    },
    level4: { 
        level1: { gift_name: { name: xx, count: xx}}, 
        level2: {}, 
        level3: {} 
    }
}
'''
'''
1: gifts 修改（数量递减）
2： gifts 奖品删除
'''

import os
import json
import time
from common.utils import check_file
from common.error import (UserExistsError, RoleError,
                           LevelError, NegativeNumberError)
from common.utils import timestamp_to_string
from common.consts import ROLES, FIRSTLEVELS, SECONDLEVELS


class Base(object):
    def __init__(self, user_json, gift_json):
        self.user_json = user_json
        self.gift_json = gift_json

        self.__check_user_json()
        self.__check_gift_json()
        self.__init_gifts()

    def __check_user_json(self):
        check_file(self.user_json)

    def __check_gift_json(self):
        check_file(self.gift_json)

    def __read_users(self, time_to_str=False):
        with open(self.user_json, 'r') as f:
            # 字符串转换为字典
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

        # 字典转换为字符串
        # json_users = json.dumps(users)
        #
        # with open(self.user_json, 'w') as f:
        #     f.write(json_users)
        self.__save(users, self.user_json)

    def __change_role(self, username, role):
        users = self.__read_users()
        print(users) # {'dewei': {'username': 'dewei', 'role': 'admin', 'active': True, 'create_time': 1650450446.281599, 'update_time': 1650508521.346771, 'gifts': []}}
        user = users.get(username)
        print(user) # {'username': 'dewei', 'role': 'admin', 'active': True, 'create_time': 1650450446.281599, 'update_time': 1650508521.346771, 'gifts': []}
        if not user:
            return False
        if role not in ROLES:
            raise RoleError('not use role %s' % role)

        user['role'] = role
        user['update_time'] = time.time()

        users[username] = user

        self.__save(users, self.user_json)
        # json_data = json.dumps(users)
        # with open(self.user_json, 'w') as f:
        #     f.write(json_data)
        return True

    def __change_active(self, username):
        users = self.__read_users()
        user = users.get(username)

        if not user:
            return False

        user['active'] = not user['active']
        user['update_time'] = time.time()

        users[username] = user

        self.__save(users, self.user_json)
        # json_data = json.dumps(users)
        # with open(self.user_json, 'w') as f:
        #     f.write(json_data)

        return True

    def __delete_user(self, username):
        users = self.__read_users()
        user = users.get(username)

        if not user:
            return False
        delete_user = users.pop(username)

        self.__save(users, self.user_json)
        # json_data = json.dumps(users)
        # with open(self.user_json, 'w') as f:
        #     f.write(json_data)

        return delete_user

    def __read_gifs(self):
        with open(self.gift_json) as f:
            data = json.loads(f.read())
        return data

    def __init_gifts(self):
        data = {
            'level1': {
                'level1': {},
                'level2': {},
                'level3': {},
            },
            'level2': {
                'level1': {},
                'level2': {},
                'level3': {},
            },
            'level3': {
                'level1': {},
                'level2': {},
                'level3': {},
            },
            'level4': {
                'level1': {},
                'level2': {},
                'level3': {},
            }
        }

        gifts = self.__read_gifs()
        if len(gifts) != 0:
            return
        self.__save(data, self.gift_json)
        # json_data = json.dumps(data)
        # with open(self.gift_json, 'w') as f:
        #     f.write(json_data)

    def __write_gift(self, first_level, second_level, gift_name, gift_count):
        # if first_level not in FIRSTLEVELS:
        #     raise LevelError('first level not exists')
        # if second_level not in SECONDLEVELS:
        #     raise LevelError('second level not exists')
        # gifts = self.__read_gifs()
        # current_gift_pool = gifts[first_level]
        # current_second_gift_pool = current_gift_pool[second_level]

        data = self.__check_and_getgift(first_level, second_level)
        if data == False:
            return data
        current_gift_pool = data.get('level_one')
        current_second_gift_pool = data.get('level_two')
        gifts = data.get('gifts')

        if gift_count <= 0:
            gift_count = 1

        if gift_name in current_second_gift_pool:
            # print(current_second_gift_pool[gift_name])
            # print(current_second_gift_pool[gift_name]['count'] + gift_count)
            current_second_gift_pool[gift_name]['count'] = current_second_gift_pool[gift_name]['count'] + gift_count
        else:
            current_second_gift_pool[gift_name] = {
                'name': gift_name,
                'count': gift_count
            }

        current_gift_pool[second_level] = current_second_gift_pool
        gifts[first_level] = current_gift_pool
        self.__save(gifts, self.gift_json)
        # json_data = json.dumps(gifts)
        # with open(self.gift_json, 'w') as f:
        #     f.write(json_data)

    def __gift_update(self, first_level, second_level, gift_name, gift_count=1):
        data = self.__check_and_getgift(first_level, second_level)
        if data == False:
            return data
        current_gift_pool = data.get('level_one')
        current_second_gift_pool = data.get('level_two')
        gifts = data.get('gifts')

        if gift_name not in current_second_gift_pool:
            return False

        current_gift = current_second_gift_pool[gift_name]

        if current_gift['count'] - gift_count < 0:
            raise NegativeNumberError('gift count can not nagative')

        current_gift['count'] -= gift_count

        current_second_gift_pool[gift_name] = current_gift
        current_gift_pool[second_level] = current_second_gift_pool
        gifts[first_level] = current_gift_pool

        self.__save(gifts, self.gift_json)

    def __delete_gift(self, first_level, second_level, gift_name):
        data = self.__check_and_getgift(first_level, second_level)
        if data == False:
            return data
        current_gift_pool = data.get('level_one')
        current_second_gift_pool = data.get('level_two')
        gifts = data.get('gifts')

        delete_gift_data = current_second_gift_pool.pop(gift_name)
        current_gift_pool[second_level] = current_second_gift_pool
        gifts[first_level] = current_gift_pool
        self.__save(gifts, self.gift_json)

        return delete_gift_data

    def __check_and_getgift(self, first_level, second_level, gift_name):
        if first_level not in FIRSTLEVELS:
            raise LevelError('first level not exists')
        if second_level not in SECONDLEVELS:
            raise LevelError('second level not exists')
        gifts = self.__read_gifs()
        level_one = gifts[first_level]
        level_two = level_one[second_level]

        if gift_name not in level_two:
            return False

        return {'level_one': level_one, 'level_two': level_two, 'gifts': gifts}

    def __save(self, data, path):
        json_data = json.dumps(data)
        with open(path, 'w') as f:
            f.write(json_data)





if __name__ == '__main__':
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    base = Base(user_path, gift_path)
    # base.write_user(username='dewei', role='admin', active=False)
    # result = base.change_role(username='dewei', role='admin')
    # print(result)
    # print(base.change_active(username='dewei'))
    # print(base.delete_user(username='dewei'))
    # print(base.read_gifs())
    # base.write_gift(first_level='level2', second_level='level3', gift_name='ipad', gift_count=30)


