"""
招生办爬虫，用于判别本科生录取信息
http://zsb.bjfu.edu.cn/f/lqcxjg
"""

import requests
import json
import base64
from bs4 import BeautifulSoup
from utils.base64ImgToText import validate_code_base64_to_str


def query_admission_info(ksh, sfzh):
    session = requests.session()
    r = session.get('http://zsb.bjfu.edu.cn/f/lqcx')

    validateCode = None

    for _ in range(3):  # 尝试多次获取并识别验证码
        req = session.get('http://zsb.bjfu.edu.cn/servlet/validateCodeServlet')
        base64_img = base64.b64encode(req.content).decode('utf-8')
        vc = validate_code_base64_to_str(base64_img)

        req = session.get(url='http://zsb.bjfu.edu.cn/servlet/validateCodeServlet?validateCode={}'.format(vc))
        # print(req.text)
        if req.text == 'true':
            validateCode = vc
            break

    if validateCode is None:
        raise Exception('网络繁忙，请稍后再试')

    data = {
        'ksh': ksh,
        'sfzh': sfzh,
        'validateCode': validateCode
    }

    req = session.post(url='http://zsb.bjfu.edu.cn/f/lqcxjg', data=data)
    bs = BeautifulSoup(req.text, 'html.parser')
    no_succ_tip = bs.find_all("div", class_="no_succ")
    if len(no_succ_tip) == 0:
        return True
    if len(no_succ_tip) == 1:
        return False