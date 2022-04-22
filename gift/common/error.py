# coding:utf-8

class NotPathError(Exception):
    def __init__(self, msg):
        self.message = msg

class FormatError(Exception):
    def __init__(self, msg = 'json format'):
        self.message = msg

class NotFileError(Exception):
    def __init__(self, msg = 'this is not file'):
        self.message = msg

class UserExistsError(Exception):
    def __init__(self, msg):
        self.message = msg

class RoleError(Exception):
    def __init__(self, msg):
        self.message = msg

class LevelError(Exception):
    def __init__(self, msg):
        self.message = msg

class NegativeNumberError(Exception):
    def __init__(self, msg):
        self.message = msg

class NotUserError(Exception):
    def __init__(self, msg):
        self.message = msg

class UserActiveError(Exception):
    def __init__(self, msg):
        self.message = msg
