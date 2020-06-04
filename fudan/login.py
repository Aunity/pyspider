#!/usr/bin/env python

import warnings
import requests
from lxml import etree

warnings.filterwarnings("ignore")


class Ehall(object):
    login_url = 'https://uis.fudan.edu.cn/authserver/login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    session = None

    def __init__(self, config):
        self.data = {
            'username': config['id'],
            'password': config['pw'],
        }

    def get_hide_paras(self):
        url = 'https://uis.fudan.edu.cn/authserver/login'
        response = self.session.get(url, headers=self.headers, verify=False)
        page_text = response.text
        html = etree.HTML(page_text)
        names = html.xpath('//*[@id="casLoginForm"]/input[@type="hidden"]/@name')
        values = html.xpath('//*[@id="casLoginForm"]/input[@type="hidden"]/@value')
        self.data.update(dict(zip(names, values)))

    def login(self):
        self.session = requests.Session()
        self.get_hide_paras()
        response = self.session.post(self.login_url, headers=self.headers, data=self.data)
        html = etree.HTML(response.text)
        username = html.xpath('// *[ @ id = "auth_siderbar"] / div[2] / span / span/text()')
        if len(username) == 0:
            print("Faild login!")
        else:
            username = username[0].strip()
            print("Successful login: %s" % username)


def main():
    import json
    loginf = 'info.login'
    with open(loginf) as fr:
        config = json.load(fr)
    ehall = Ehall(config)
    ehall.login()


if __name__ == "__main__":
    main()
