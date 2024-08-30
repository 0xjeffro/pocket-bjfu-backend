# -*- coding: utf-8 -*-
import requests
import json


url = "http://bjfu.sunnysport.org.cn/login/"


def sunny_run(username):
    try:
        info = requests.get(url="http://bjfu.sunnysport.org.cn/api/student/info/{}".format(username)).json()
        if info.get("state", "") == '该用户不存在':
            return ""

        group = requests.get(url="http://bjfu.sunnysport.org.cn/api/student/group/{}".format(username)).json()
        achievements = requests.get(url="http://bjfu.sunnysport.org.cn/api/student/achievements/{}".format(username)).json()

        achievements.reverse()
        data = dict()
        data['success'] = True
        data["info"] = info
        data["group"] = group
        data["achievements"] = achievements
        return data
    except Exception as e:
        return {'success': False}


if __name__ == '__main__':
    print(sunny_run("190400212"))

"""
data = {
    'info': {
        'validTimes': '30',
        'code': '190400601',
        'name': '周默',
        'speed': '1.8707022369066746',
        'mileages': '60000',
        'validMileages': '60000',
        'rand': '0',
        'todaymileage': 0,
        'todayspeed': 0
    },
    'group': {
        'code': '190400601',
        'name': '周默',
        'claz': '工商类19-6',
        'college': '经济管理学院',
        'teacher': '刘东',
        'times': '22',
        'speed': '1.7',
        'group': 'Default_Male',
        'mileage': '2000.0'
    },
    'achievements': [{
        'mileage': 2000,
        'code': '190400601',
        'isValid': True,
        'date': '2020-10-05',
        'domain': '下午',
        'speed': 1.95121951219512
    }, {
        'mileage': 2000,
        'code': '190400601',
        'isValid': True,
        'date': '2020-10-23',
        'domain': '下午',
        'speed': 1.9782393669634
    }, {
        'mileage': 2000,
        'code': '190400601',
        'isValid': True,
        'date': '2020-10-25',
        'domain': '下午',
        'speed': 1.82149362477231
    }, {
        'mileage': 2000,
        'code': '190400601',
        'isValid': True,
        'date': '2020-10-26',
        'domain': '下午',
        'speed': 1.75901495162709
    }, {
        'mileage': 0,
        'code': '190400601',
        'isValid': False,
        'date': '2020-11-09',
        'domain': '下午',
        'speed': 0.0
    }, {
        'mileage': 2000,
        'code': '190400601',
        'isValid': True,
        'date': '2020-11-10',
        'domain': '下午',
        'speed': 1.79533213644524
    }]
}
"""