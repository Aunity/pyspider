#!/usr/bin/env python
#! -*- coding: utf-8 -*-
'''
@Time    : 2020/7/1 15:03
@Author  : MaohuaYang
@Contact : maohuay@hotmail.com 
@File    : API.py
@Software: PyCharm
'''
import json
import pymysql
import requests

class PMC(object):
    api_url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search'
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Host': 'www.ebi.ac.uk',
        "Connection": 'keep-alive',
    }
    def __init__(self):
        self.session = requests.Session()
        self.paras = {
            "query": "",
            "resultType": "core",
            "synonym": "false",
            "cursorMark": "*",
            "pageSize": "75",
            "sort": "P_PDATE_D asc",
            "format": "json",
        }

    def __set_paras(self, k, v):
        self.paras[k] = v

    def __post(self):
        response = self.session.get(self.api_url, headers=self.headers, params=self.paras)
        # print(response.url)
        return response

    def __parse_response(self, response):
        page_json = response.json()
        print(page_json["hitCount"],page_json['request'])
        return page_json['nextCursorMark']

    def query(self, keyword):
        self.paras['query'] = keyword
        while 1:
            response = self.__post()
            cursorMark = self.__parse_response(response)
            if cursorMark == self.paras['cursorMark']:
                break
            else:
                self.paras['cursorMark'] = cursorMark

    def to_mysql(self):
        # conn = pymysql.
        pass

    def to_csv(self):
        pass


def main():
    pmc = PMC()
    pmc.query("IDP and molecular simulation")
if __name__ == "__main__":
    main()