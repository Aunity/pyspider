#!/usr/bin/env python
#! -*- coding: utf-8 -*-
'''
@Time    : 2020/7/9 18:40
@Author  : MaohuaYang
@Contact : maohuay@hotmail.com 
@File    : api.py
@Software: PyCharm
'''

import time
import execjs

import codecs
import base64
import hashlib
import numpy as np
from Crypto.Cipher import AES
from .base import BaseLogin


class AcFun(BaseLogin):

    def login(self):
        url = "https://id.app.acfun.cn/rest/web/login/signin"
        paras = {
            "username": self.username,
            "password": self.password,
            "key": "",
            "captcha": ""
        }
        response = self.session.post(url, headers=self.headers, data=paras)
        page_json = response.json()
        if page_json['result'] == 0:
            print("Login sucessful！%s" % page_json['username'])
        else:
            print("Faild login")

    def __get_time_str(self):
        tmp = str(time.time())
        tmp = tmp.split(".")
        return tmp[0] + tmp[1][:3]

    def sign_in(self):
        curtime = self.__get_time_str()
        ext = execjs.compile('''
                    function gene_cert(){
                        return Math.random().toString(36).substr(2)
                    }
        ''')
        certified = ext.call("gene_cert").encode('utf-8')
        certified = base64.b64encode(certified)
        self.session.cookies.update({'stochastic': str(certified)})
        url = r"https://www.acfun.cn/nd/pst?locationPath=signin&certified=%s&channel=0&data=%s" % (certified, curtime)
        response = self.session.post(url, headers=self.headers)
        print(response.json()['message'])




class Music163(BaseLogin):

    def __init__(self, config):
        self.headers.update({
            'content-type': "application/x-www-form-urlencoded",
            "referer": "https://music.163.com/"
        })
        self.random_key = None
        BaseLogin.__init__(self, config)

    def __get_random_key(self, length):
        s1, var0 = "", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        for i in range(length):
            ndx = np.random.randint(0, len(var0))
            s1 += var0[ndx]
        self.random_key = s1
        return s1

    def __AES_encrypt(self, data, key="0CoJUm6Qyw8W8jud"):
        iv = "0102030405060708"
        pad = 16 - len(data) % 16
        if isinstance(data, str):
            text = data + pad * chr(pad)
        else:
            text = data.deocde("utf-8") + pad * chr(pad)

        aes = AES.new(key=bytes(key, encoding='utf-8'), mode=AES.MODE_CBC, IV=bytes(iv, encoding='utf-8'))
        text = bytes(text, encoding="utf-8")
        res = aes.encrypt(text)
        res = base64.b64encode(res).decode("utf-8")
        return res

    def __get_encText(self, text):
        key = self.__get_random_key(16)
        encText = self.__AES_encrypt(text)
        return self.__AES_encrypt(encText, key=key)


    def __get_encSecKey(self):
        if self.random_key is None:
            self.__get_random_key(16)
        random_key = self.random_key[::-1]
        e, f = "010001", "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        rs = int(codecs.encode(random_key.encode('utf-8'), 'hex_codec'), 16) ** int(e, 16) % int(f, 16)
        return format(rs, 'x').zfill(256)

    def login(self):
        args = '{"phone":"%s","password":"%s","rememberLogin":"true","checkToken":"","csrf_token": ""}' % (
            self.username, hashlib.md5(bytes(self.password, encoding="utf-8")).hexdigest())
        data = {
            "params": self.__get_encText(args),
            "encSecKey": self.__get_encSecKey()
        }
        url = "https://music.163.com/weapi/login/cellphone"
        response = self.session.post(url, data=data, headers=self.headers)
        page_json = response.json()
        if page_json['code'] == 200:
            print(page_json['profile']['nickname'], '登录成功！')
        else:
            print(page_json["msg"])

    def sign_in(self):
        url = "https://music.163.com/weapi/point/dailyTask"
        csrf_token = self.session.cookies.get("__csrf")
        url = "https://music.163.com/weapi/point/dailyTask?csrf_token=%s" % csrf_token
        args = '{"type":1,"csrf_token":"%s"}' % csrf_token
        data = {
            "params": self.__get_encText(args),
            "encSecKey": self.__get_encSecKey()
        }
        response = self.session.post(url, headers=self.headers, data=data)
        page_json = response.text
        print(page_json)

    def crawl_music_comments(self):
        '''
        依据歌曲ID爬取该歌曲的评论
        :return:
        '''
        url = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_1321007185"
        args = '{"rid":"R_SO_4_1321007185","offset":"0","total":"true","limit":"20","csrf_token":""}'
        data = {
            "params": self.__get_encText(args),
            "encSecKey": self.__get_encSecKey()
        }
        response = self.session.post(url, headers=self.headers, data=data)
        page_json = response.json()
        print(page_json)