import json
from datetime import datetime

import requests

from .accessToken import get_access_token


def send_reply_subscribe_message(toUser, page, text):
    try:
        template_id = 'mcVxahzO9c1kmGRGIPNqcpl-ktqYudlqWmh55osOMxs'
        if len(text) > 15:
            text = text[:15] + '...'

        access_token = get_access_token()

        req = requests.post(
            'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={0}'.format(access_token),
            data=json.dumps({
                'access_token': access_token,
                'touser': toUser,
                'template_id': template_id,
                'page': page,
                'data': {
                    'thing2': {
                        'value': text
                    },
                    'date3': {
                        'value':  datetime.now().strftime('%Y-%m-%d %H:%M')
                    }
                },
                'miniprogram_state': 'formal'
            }))
        return
    except Exception as e:
        return
