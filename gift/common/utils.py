# coding:utf-8

import os
from .error import NotFileError, NotPathError, FormatError

def check_file(path):
    if not os.path.exists(path):
        raise NotPathError('not found %s' % path)

    if not path.endswith('.json'):
        raise FormatError()

    if not os.path.isfile(path):
        raise NotFileError()