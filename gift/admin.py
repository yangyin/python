# coding:utf-8

'''
1: admin类的搭建
2：获取用户函数（包含获取身份）
3：添加用户（判断当前身份是否是管理员）
4：冻结与恢复用户
5：修改用户身份
'''
from base import Base
import os
from common.error import NotUserError, UserActiveError



class Admin(Base):
    def __init__(self, username, user_json, gift_json):
        self.username = username
        super().__init__(user_json, gift_json)
        self.get_user()

    def get_user(self):
        users = self._Base__read_users()
        current_user = users.get(self.username)

        if current_user == None:
            raise NotUserError('not user %s' % self.username)
        if current_user.get('active') == False:
            raise UserActiveError('this user %s had not use' % self.username)
        self.user = current_user
        self.role = current_user.get('role')
        self.name = current_user.get('username')
        self.active = current_user.get('active')

    def add_user(self, username, role):
        if self.role != 'admin':
            raise Exception('permission')
        self._Base__write_user(username=username, role=role)

    def update_user_active(self, username):
        if self.role != 'admin':
            raise Exception('permission')

        self._Base__change_active(username=username)

    def update_user_role(self, username, role):
        if self.role != 'admin':
            raise Exception('permission')
        self._Base__change_role(username=username, role=role)




if __name__ == '__main__':
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    admin = Admin('dewei', user_json=user_path, gift_json=gift_path)
    # admin.add_user(username='xiaomu', role='admin')
    admin.update_user_active('xiaomu')
    admin.update_user_role('xiaomu', role='normal')