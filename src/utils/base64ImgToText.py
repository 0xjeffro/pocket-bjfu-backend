"""
将base64编码的图片调用api转化为文字（验证码识别）
"""

import requests


def validate_code_base64_to_str(img_base64):
    from datetime import datetime as pydatetime
    import ssl, hmac, base64, hashlib

    secretId = "AKID99rYDkroejz4xo7gcf4l6lxJz92fxXj4hqk3"
    secretKey = "I78G86HawM1q1rwj6kopi9sAZzJEnoEuDnn01v0Z"
    source = "market"
    datetime = pydatetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    signStr = "x-date: %s\nx-source: %s" % (datetime, source)
    sign = base64.b64encode(hmac.new(secretKey.encode('utf-8'), signStr.encode('utf-8'), hashlib.sha1).digest())
    auth = 'hmac id="%s", algorithm="hmac-sha1", headers="x-date x-source", signature="%s"' % (
    secretId, sign.decode('utf-8'))
    headers = {
        'X-Source': source,
        'X-Date': datetime,
        'Authorization': auth,
    }
    bodyParams = {
        "number": 4,
        "pri_id": "ne",
        "v_pic": img_base64
    }
    url = 'http://service-98wvmcga-1256810135.ap-guangzhou.apigateway.myqcloud.com/release/yzm'
    req = requests.post(url=url, headers=headers, data=bodyParams)
    return req.json()['v_code']