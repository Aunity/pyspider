#!/usr/bin/env python
# ! -*- coding: utf-8 -*-
'''
@Time    : 2020/6/4 16:33
@Author  : MaohuaYang
@Contact : maohuay@hotmail.com
@File    : pinganFudan-GUI.py
@Software: PyCharm
'''

import time
import requests
import tkinter as tk
from login import Ehall

def set_win_center(root, curWidth='', curHight=''):
    """
   设置窗口大小，并居中显示
    :param root:主窗体实例
    :param curWidth:窗口宽度，非必填，默认200
    :param curHight:窗口高度，非必填，默认200
    :return:无
   """
    if not curWidth:
        '''获取窗口宽度，默认200'''
        curWidth = root.winfo_width()
    if not curHight:
        '''获取窗口高度，默认200'''
        curHight = root.winfo_height()
    # print(curWidth, curHight)

    # 获取屏幕宽度和高度
    scn_w, scn_h = root.maxsize()
    # print(scn_w, scn_h)

    # 计算中心坐标
    cen_x = (scn_w - curWidth) / 2
    cen_y = (scn_h - curHight) / 2
    # print(cen_x, cen_y)

    # 设置窗口初始大小和位置
    size_xy = '%dx%d+%d+%d' % (curWidth, curHight, cen_x, cen_y)
    root.geometry(size_xy)

def sign_up(ehall, address_info):
    url = 'https://zlapp.fudan.edu.cn/ncov/wap/fudan/get-info'
    response = ehall.session.get(url, headers=ehall.headers, verify=False)
    data = response.json()

    url = 'https://zlapp.fudan.edu.cn/ncov/wap/fudan/save'
    data['d']['info'].update(address_info)
    post_data = data['d']['info']
    response = ehall.session.post(url, data=post_data, verify=False, headers=ehall.headers)

    return response.json()


def main():
    root = tk.Tk()
    root.title("DailyFudan")
    set_win_center(root, 700, 350)
    root.resizable(0, 0)

    # user ID
    lblid  = tk.Label(root, text="学号：")
    lblid.grid(row=0, column=0)
    #lid.pack()

    entID = tk.Entry(root)
    entID.grid(row=0, column=1, padx=25, pady=0)
    #entID.pack()
    # password
    lblPW = tk.Label(root, text="Ehall密码：")
    lblPW.grid(row=1, column=0)
    #lPW.pack()
    entPW = tk.Entry(root, show="*")
    entPW.grid(row=1, column=1)
    #entPW.pack()

    # location information
    lblArea = tk.Label(root, text='区域：')
    lblArea.grid(row=2, column=0)
    varArea = tk.StringVar(value="上海市 杨浦区")
    entArea = tk.Entry(root, textvariable=varArea,  width=20)
    entArea.grid(row=2, column=1)
    #entArea.pack()
    lblProv = tk.Label(root, text='省份：')
    lblProv.grid(row=3, column=0)
    varProv = tk.StringVar(value="上海")
    entProv = tk.Entry(root, textvariable=varProv,  width=20)
    entProv.grid(row=3, column=1)
    #entProv.pack()
    lblCity = tk.Label(root, text='城市：')
    lblCity.grid(row=4, column=0)
    varCity = tk.StringVar(value="上海市")
    entCity = tk.Entry(root, textvariable=varCity,  width=20)
    entCity.grid(row=4, column=1)
    #entCity.pack()

    # auto submit
    # to be continue

    # log area
    scroll = tk.Scrollbar()

    textlog = tk.Text(root, state=tk.DISABLED, width=50, bg='lightgray')
    textlog.grid(row=0, rowspan=6, column=2, sticky=tk.S+tk.W+tk.E+tk.N)
    scroll.grid(row=0, rowspan=6, column=3, sticky=tk.S + tk.W + tk.E + tk.N, ipadx=0)
    scroll.config(command=textlog.yview)
    textlog.config(yscrollcommand=scroll.set)

    def submit_btn_cmd():
        id = entID.get().strip()
        pw = entPW.get().strip()
        config = {
            'id': id,
            'pw': pw
        }
        ehall = Ehall(config)
        ehall.login()
        if ehall.username:
            address_info = {
                "area": varArea.get(),
                "province": varProv.get(),
                "city": varCity.get()
            }
            data = sign_up(ehall, address_info)
            print(data)
            if data['e'] == 0:
                log = ">>填报成功！%s    %s\n" % (ehall.username, time.ctime())
            else:
                log = ">>今日已填报！%s    %s\n" % (ehall.username, time.ctime())
        else:
            log = ">>登录失败！%s    %s\n" % (ehall.username, time.ctime())
        textlog.config(state=tk.NORMAL)
        textlog.insert("insert", log)
        textlog.config(state=tk.DISABLED)

    btuExit = tk.Button(root, text='退出', command=root.quit,  width=10)
    btuExit.grid(row=5, column=1, pady=2)
    btuSub = tk.Button(root, text="提交", command=submit_btn_cmd, width=10)
    btuSub.grid(row=5, column=0, pady=2, padx=20)

    root.mainloop()


if __name__ == "__main__":
    main()
