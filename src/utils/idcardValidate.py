import ssl, hmac, base64, hashlib
from datetime import datetime as pydatetime
import requests


def idcard_validate(idcard_number, name):
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
        "idcard_number": idcard_number,
        "name": name
    }
    url = 'https://service-g5hqhvkd-1305308687.sh.apigw.tencentcs.com/release/idcard/validate'
    req = requests.post(url=url, headers=headers, data=bodyParams)
    return req.json()['success']