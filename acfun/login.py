#!/usr/bin/env python
#! -*- coding: utf-8 -*-
'''
@Time    : 2020/6/9 18:23
@Author  : MaohuaYang
@Contact : maohuay@hotmail.com 
@File    : login.py
@Software: PyCharm
'''

import requests

class AcFun(object):
    headers = {
        'user-agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    }
    session = requests.session()
    def __init__(self, config):
        self.username = config['username']
        self.passwd = config['passwd']


    def login(self):
        url = "https://id.app.acfun.cn/rest/web/login/signin"
        paras = {
            "username": self.username,
            "password": self.passwd,
            "key": "",
            "captcha": ""
        }
        response = self.session.post(url, headers=self.headers, data=paras)
        print(response.text)

    def sign_in(self):
        pass

def main():
    import json
    loginf = 'info.login'
    with open(loginf) as fr:
        config = json.load(fr)
    acfun_login = AcFun(config)
    acfun_login.login()

if __name__ == "__main__":
    main()