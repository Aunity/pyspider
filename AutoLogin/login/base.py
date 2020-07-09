#!/usr/bin/env python
# ! -*- coding: utf-8 -*-
'''
@Time    : 2020/7/8 11:26
@Author  : MaohuaYang
@Contact : maohuay@hotmail.com 
@File    : headers.py
@Software: PyCharm
'''
import requests
from ..headers.UA import seed_UA


class BaseLogin(object):
    headers = {
        'user-agent': seed_UA(UA_type='PC')
    }
    session = None

    def __init__(self, config):
        self.username = config['username']
        self.password = config['passwd']
        self.session = requests.session()

    def login(self):
        pass
