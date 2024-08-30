import requests
import json
from urllib.parse import quote

# 飞书APP配置
APP_ID = "cli_a0804e0a6035100d"
APP_SECRET = "4wfe2WfJmYluTEBR5TG8MhBuX3vIYEAh"

# 消息接收人的OPEN_ID
OPEN_ID = "ou_236eff47758c713892fe47c3348b92e5"


def get_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    req_body = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    try:
        req = requests.post(url=url, params=req_body)
        data = json.loads(req.text)
        if data['code'] == 0:
            return data["tenant_access_token"]
        else:
            # print("get tenant_access_token error, code =", data['code'])
            return ""
    except Exception as e:
        # print(e)
        return ""


def get_open_id_by_phone(phoneNumber):
    """
    根据手机号获取用户open_id
    :param phoneNumber:
    :return:
    """
    url = 'https://open.feishu.cn/open-apis/user/v1/batch_get_id'
    token = get_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    req_body = {
        "mobiles": quote(phoneNumber)
    }

    req = requests.get(url=url, params=req_body, headers=headers)
    data = json.loads(req.text)
    print(data)


def send_feishu_msg(msg):
    url = "https://open.feishu.cn/open-apis/message/v4/send/"
    token = get_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    req_body = {
        "open_id": OPEN_ID,
        "msg_type": "text",
        "content": {
            "text": msg
        }
    }
    try:
        req = requests.post(url=url, data=json.dumps(req_body), headers=headers)
        data = req.json()
        if data['code'] != 0:
            return 'get tenant_access_token error'
            # print("get tenant_access_token error, code =", data['code'])
    except Exception as e:
        # print(e)
        return str(e)
