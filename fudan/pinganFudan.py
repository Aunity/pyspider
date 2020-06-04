#!/usr/bin/env python

import json
from login import Ehall

def main():
    url = 'https://zlapp.fudan.edu.cn/ncov/wap/fudan/get-info'
    with open('./info.login') as fr:
        config = json.load(fr)
    ehall = Ehall(config)
    ehall.login()
    response = ehall.session.get(url, headers=ehall.headers, verify=False)
    response.coding = 'utf-8'
    data = response.json()
    print(data)
    with open('basicinfo.json','w', encoding='utf-8') as fw:
        json.dump(data, fw , ensure_ascii=False, indent=4)
    with open('basicinfo.json', encoding='utf-8') as fr:
        data = json.load(fr)
    print(data)

    url = 'https://zlapp.fudan.edu.cn/ncov/wap/fudan/save'
    address_info ={
        "area": "上海市 杨浦区",
        "province": "上海市",
        "city": "上海市"
    }
    data['d']['info'].update(address_info)
    post_data = data['d']['info']
    response = ehall.session.post(url, data=post_data, verify=False, headers=ehall.headers)
    daliylog = "submit.log"
    with open(daliylog, 'w+', encoding='utf-8') as fw:
        json.dump(response.json(), fw, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    main()