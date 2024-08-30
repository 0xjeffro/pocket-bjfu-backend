from django.conf import settings
from services.QZAPI import SW
from services.QZSPIDER import QZSpider
import redis


def interface_verify(xh, pwd):
    """
    验证学号和密码的正确性

    :param xh: 学号
    :param pwd: 密码
    :return:
        0: 学号密码正确，登录成功
        1: 学号或密码错误，登录失败
        -1: 接口调用失败
    """
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.DB, password=settings.REDIS_PWD)
    url = r.get('vpnUrl')
    # url = url.decode('utf-8') + '/app.do'
    # Q = SW(xh, pwd, url)
    # return Q.login()
    """
    API不可用，切换到爬虫验证
    """
    Q = QZSpider(xh, pwd, url.decode('utf-8'))
    return Q.login()






def interface_cj(xh, pwd, xnxq):
    """
    获取成绩

    :param xh: 学号
    :param pwd: 密码
    :param xnxq: 学年学期，如：2019-2020-1 2017-2018-3
    :return:
        成功：
            {
                'success': True,
                'result': [{
                    'bz': None,
                    'kclbmc': '必修',
                    'zcj': '85',
                    'xm': '周默',
                    'xqmc': '2020-2021-1',
                    'kcxzmc': '专业基础课',
                    'kcywmc': 'Introduction to Management Model and Decision Making',
                    'ksxzmc': '正常考试',
                    'kcmc': '管理模型与决策基础',
                    'xf': 3,
                    'cjbsmz': None
                }, {
                    'bz': None,
                    'kclbmc': '公选',
                    'zcj': '不合格',
                    'xm': '周默',
                    'xqmc': '2020-2021-1',
                    'kcxzmc': None,
                    'kcywmc': 'Indoor Flowers and Decoration(Online Course)',
                    'ksxzmc': '正常考试',
                    'kcmc': '室内花卉与装饰（视频课）',
                    'xf': 1,
                    'cjbsmz': None
                }
            }
        失败： {"success": False}

    """

    """
        redis中关于成绩的key:
            cj_{{xh}}_{{xnxq}}_cache 例：cj_171002412_2020-2021-1_cache  暂时缓存
        
        请求逻辑：
            1. 如果找到 key2 直接返回，这是缓存，防止用户暴力请求，要设置过期时间
            2. 如果没找到key2 请求教务处返回，期间将缓存结果放入key2
    """
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.DB, password=settings.REDIS_PWD)
    url = r.get('vpnUrl')

    # 调用api
    # url = url.decode('utf-8') + '/app.do'
    # cache = r.get('cj_{0}_{1}_cache'.format(xh, xnxq))
    # if cache is not None:
    #     return eval(cache)
    # else:
    #     Q = SW(xh, pwd, url)
    #     Q.login()
    #     data = Q.get_cj(xnxq)
    #     if data['success']:
    #         r.set('cj_{0}_{1}_cache'.format(xh, xnxq), str(data), ex=300)
    #     return data

    # 调用爬虫
    url = url.decode('utf-8')
    cache = r.get('cj_{0}_{1}_cache'.format(xh, xnxq))
    if cache is not None:
        return eval(cache)
    else:
        Q = QZSpider(usr=xh, pwd=pwd, url=url)
        Q.login()
        data = Q.get_cj(xnxq=xnxq)
        if data['success']:
            r.set('cj_{0}_{1}_cache'.format(xh, xnxq), str(data), ex=300)
        return data


def interface_kcb(xh, pwd, currentWeek):
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.DB,
                          password=settings.REDIS_PWD)
    url = r.get('vpnUrl')
    jwxt_url = url.decode('utf-8')
    api_url = url.decode('utf-8') + '/app.do'
    cache = r.get('kcb_{0}_{1}_cache'.format(xh, currentWeek))

    if cache is not None:
        return eval(cache)
    else:
        if int(currentWeek) <= 19:  # 当周次小于19周时正常请求api
            # Q = SW(xh, pwd, api_url)
            # Q.login()
            # data = Q.get_kcb(settings.XNXQID, currentWeek)

            Q = QZSpider(usr=xh, pwd=pwd, url=jwxt_url)
            Q.login()
            data = Q.get_summer_kcb(xnxqh='2021-2022-1', week=int(currentWeek))
        else:  # 否则是暑期学期，调用爬虫
            Q = QZSpider(usr=xh, pwd=pwd, url=jwxt_url)
            Q.login()
            data = Q.get_summer_kcb(xnxqh='2020-2021-3', week=int(currentWeek) - 19)  # 注意week传参，用currentWeek - 19
        if data['success']:
            r.set('kcb_{0}_{1}_cache'.format(xh, currentWeek), str(data), ex=14400)
        return data


def interface_pm(xh, pwd):
    """
    redis中关于排名的key:
    pm_{{xh}}_cache
    :param xh: 学号
    :param pwd: 密码
    :return:
    """
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.DB, password=settings.REDIS_PWD)
    url = r.get('vpnUrl')
    url = url.decode('utf-8')
    cache = r.get('pm_{0}_cache'.format(xh))
    if cache is not None:
        return eval(cache)
    else:
        Q = QZSpider(usr=xh, pwd=pwd, url=url)
        Q.login()
        data = Q.get_pm()
        if data['success']:
            r.set('pm_{0}_cache'.format(xh), str(data), ex=300)
        return data


def interface_kjs(xh, pwd, xnxqh, zc, xq, _jc, jxl):
    """
        redis中关于排名的key:
        kjs_{{xnxqh}}_{{zc}}_{{xq}}_{{jc}}_{{jc2}}_{{jxl}_cache
      :param xh: 学号
      :param pwd: 密码
      :param xnxqh: 学年学期号 2020-2021-1
      :param zc: 周次 1，2，3，4，5，6，7，8... 15，16，17，18，...
      :param xq: 星期: 1，2，3，4，5，6，7
      :param _jc: 节次:
        0: 1-2
        1: 3-4
        2: 5
        3: 6-7
        4: 8-9
        5: 10-12
      :param jxl: 全部: 0 一教：1, 二教: 2, 学研：3
        :return:
    """
    jc = '1'
    jc2 = '2'

    if str(_jc) == '0':
        jc = '1'
        jc2 = '2'
    elif str(_jc) == '1':
        jc = '3'
        jc2 = '4'
    elif str(_jc) == '2':
        jc = '5'
        jc2 = '5'
    elif str(_jc) == '3':
        jc = '6'
        jc2 = '7'
    elif str(_jc) == '4':
        jc = '8'
        jc2 = '9'
    elif str(_jc) == '5':
        jc = '10'
        jc2 = '12'

    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.DB, password=settings.REDIS_PWD)
    url = r.get('vpnUrl')
    url = url.decode('utf-8')
    cache = r.get('kjs_{0}_{1}_{2}_{3}_{4}_{5}_cache'.format(xnxqh, zc, xq, jc, jc2, jxl))
    if cache is not None:
        return eval(cache)
    else:
        Q = QZSpider(usr=xh, pwd=pwd, url=url)
        Q.login()
        jxlbh = '001'
        if str(jxl) == '0':
            jxlbh = ''
        elif str(jxl) == '1':
            jxlbh = '001'
        elif str(jxl) == '2':
            jxlbh = '003'
        elif str(jxl) == '3':
            jxlbh = '014'

        data = Q.get_kjs(xnxqh=settings.XNXQID, jxlbh=jxlbh, zc=zc, zc2=zc, xq=xq, xq2=xq,
                         jc=str(jc).zfill(2), jc2=str(jc2.zfill(2)))
        if data['success']:
            r.set('kjs_{0}_{1}_{2}_{3}_{4}_{5}_cache'.format(xnxqh, zc, xq, jc, jc2, jxl), str(data), ex=3600)
        return data
