#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import requests
import re
import os
import json
import datetime


class SW(object):
    """docstring for SW"""

    def __init__(self, account, password, url):
        super(SW, self).__init__()
        self.name = ""  # 姓名
        self.academy = ""  # 学院
        self.kb = ""  # 课表
        self.cj = ""  # 成绩
        self.account = account
        self.password = password
        self.success = False  # 是否成功登录
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Linux; U; Mobile; Android 6.0.1;C107-9 Build/FRF91 )',
            'Referer': 'http://www.baidu.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh-TW;q=0.8,zh;q=0.6,en;q=0.4,ja;q=0.2',
            'cache-control': 'max-age=0'
        }
        self.xnxq = ["2018-2019-3", "2018-2019-2", "2018-2019-1"]
        self.url = url

    def login(self):
        """

        :return:
         1: 登录成功
         0: 密码错误
         -1: 系统繁忙
        """
        params = {
            "method": "authUser",
            "xh": self.account,
            "pwd": self.password
        }
        try:
            req = requests.get(url=self.url, params=params, timeout=3, headers=self.HEADERS)
            s = json.loads(req.text)

            if s['success'] is False:  # 返回False说明api可用，但用户名，密码有误
                return {
                    'success': False
                }
            else:  # 登录成功，记录姓名学院，把登录成功标记为true
                self.name = s["user"]["username"]
                self.academy = s["user"]["userdwmc"]
                self.success = True
                self.HEADERS['token'] = s['token']
                return {
                    'success': True,
                    'name': self.name,
                    'academy': self.academy
                }
        except Exception as e:
            return -1

    def get_handle(self, params):
        req = requests.get(self.url, params=params, timeout=3, headers=self.HEADERS)
        return req

    def get_current_time(self):  # 获取当前时间
        """
        仅作测试用，学年学期、周次等根据实际情况计算
        :return:
            {"zc":19,"e_time":"2021-01-24","s_time":"2021-01-19","xnxqh":"2020-2021-1"}
        """
        try:
            params = {
                "method": "getCurrentTime",
                "currDate": (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime('%Y-%m-%d')
            }
            req = self.get_handle(params)
            return req.text
        except Exception as e:
            return ""

    def get_kcb(self, xnxq, zc):  # 获取课表
        if self.success is False:
            return {
                'success': False
            }
        try:
            params = {
                "method": "getKbcxAzc",
                "xnxqid": xnxq,
                "zc": zc,
                "xh": self.account
            }
            req = self.get_handle(params)
            self.kb = req.text
            return {
                'success': True,
                'kcb': req.json()
            }
        except Exception as e:
            return {
                'success': False
            }

    def get_cj(self, xnxq):  # 成绩查询
        try:
            params = {
                "method": "getCjcx",
                "xh": self.account,
                "xnxqid": xnxq
            }
            req = self.get_handle(params)
            return req.json()
        except Exception as e:
            return {'success': False}


if __name__ == '__main__':
    Q = SW("191701105", "sheng03zhu5098@", "http://ymq-manage.natapp1.cc/app.do")

    print(Q.login())
    print(Q.get_cj(xnxq="2020-2021-2"))
    print(Q.get_kcb(xnxq="2020-2021-1", zc="18")) #当前周次课表
    #print(Q.get_cj("2020-2021-1")) #成绩查询