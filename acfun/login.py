#!/usr/bin/env python
#! -*- coding: utf-8 -*-
'''
@Time    : 2020/6/9 18:23
@Author  : MaohuaYang
@Contact : maohuay@hotmail.com 
@File    : login.py
@Software: PyCharm
'''

import time
import execjs
import base64
import requests


class AcFun(object):
    headers = {
        'user-agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    }
    session = None
    def __init__(self, config):
        self.username = config['username']
        self.passwd = config['passwd']
        self.session = requests.session()

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

    def __get_time_str(self):
        tmp = str(time.time())
        tmp = tmp.split(".")
        return tmp[0]+tmp[1][:3]
    def sign_in(self):
        curtime = self.__get_time_str()
        ext = execjs.compile('''
                    function gene_cert(){
                        return Math.random().toString(36).substr(2)
                    }
        ''')
        certified = ext.call("gene_cert").encode('utf-8')
        certified = base64.b64encode(certified)
        print(certified)
        self.session.cookies.update({'stochastic':str(certified)})
        #url = "https://www.acfun.cn/nd/pst?"
        #response = self.session.post(url, data=paras, headers=self.headers)
        url = r"https://www.acfun.cn/nd/pst?locationPath=signin&certified=%s&channel=0&data=%s"%(certified, curtime)
        response = self.session.post(url, headers=self.headers)
        print(response.url)
        print(response.json())

def main():
    import json
    loginf = 'info.login'
    with open(loginf) as fr:
        config = json.load(fr)
    acfun_login = AcFun(config)
    acfun_login.login()
    acfun_login.sign_in()

if __name__ == "__main__":
    main()