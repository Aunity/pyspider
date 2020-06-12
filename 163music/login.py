#/usr/bin/env python
'''
@Time    : 2020/6/8 14:23
@Author  : MaohuaYang
@Contact : maohuay@hotmail.com
@File    : login.py
@Software: PyCharm
'''

'''
参考：
    https://www.cnblogs.com/zhuchunyu/p/10978093.html
'''
import json
import codecs
import base64
import hashlib
import requests
import numpy as np
from Crypto.Cipher import AES


class Music163(object):
    session = requests.Session()
    random_key = None
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'content-type': "application/x-www-form-urlencoded",
        "referer": "https://music.163.com/"
    }

    def __init__(self, config):
        self.username = config['id']
        self.password = config['pw']

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

    def __get_encText(self):
        key = self.__get_random_key(16)
        args = '{"phone":"%s","password":"%s","rememberLogin":"true","checkToken":"","csrf_token": ""}' % (
            self.username, hashlib.md5(bytes(self.password, encoding="utf-8")).hexdigest())
        encText = self.__AES_encrypt(args)
        return self.__AES_encrypt(encText, key=key)


    def __get_encSecKey(self):
        if self.random_key is None:
            self.__get_random_key(16)
        random_key = self.random_key[::-1]
        e, f = "010001", "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        rs = int(codecs.encode(random_key.encode('utf-8'), 'hex_codec'), 16) ** int(e, 16) % int(f, 16)
        return format(rs, 'x').zfill(256)

    def login(self):
        data = {
            "params": self.__get_encText(),
            "encSecKey": self.__get_encSecKey()
        }
        url = "https://music.163.com/weapi/login/cellphone"
        response = self.session.post(url, data=data, headers=self.headers)
        print(response.json())
        page_json = response.json()
        if page_json['code'] == 200:
            print(page_json['profile']['nickname'], '登录成功！')
        else:
            print(page_json["msg"])
        # daliylog = "response.log"
        # with open(daliylog, 'w+', encoding='utf-8') as fw:
        #     json.dump(response.json(), fw, ensure_ascii=False, indent=4)

def main():
    loginf = 'info.login'
    with open(loginf) as fr:
        config = json.load(fr)
    loginm = Music163(config)
    loginm.login()

if __name__ == "__main__":
    main()