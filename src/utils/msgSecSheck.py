from .accessToken import get_access_token
import requests
import json
import datetime
from apps.rules.models import KeyWords
from apps.users.models import UserProfile
from utils.FeiShuMessage import send_feishu_msg


def msg_sec_check(text):
    try:
        access_token = get_access_token()
        data = json.dumps({
            'content': text
        }, ensure_ascii=False).encode('utf-8')
        req = requests.post('https://api.weixin.qq.com/wxa/msg_sec_check?access_token={0}'.format(access_token),
                            data=data)
        req_json = req.json()
        if req_json['errcode'] == 87014:
            return 0
        else:
            return 1
    except Exception as e:
        return 1


def key_words_check(text, openId, scenes):
    content_state, comment_state, priority_delta = '1', '1', 0

    key_words = KeyWords.objects.filter(valid_time_to__gte=datetime.datetime.now())
    for key_word in key_words:
        if text.find(key_word.keyword) != -1:

            if content_state != '0' and comment_state != '3':
                content_state = key_word.content_state

            if comment_state != '0':
                comment_state = key_word.comment_state

            if key_word.priority_delta > 0:
                priority_delta = key_word.priority_delta
            else:
                priority_delta = min(priority_delta, key_word.priority_delta)

            if key_word.if_notice is True:
                user = UserProfile.objects.get(openId=openId)
                real_name, academy, xh = user.realName, user.academy, user.xh
                try:
                    send_feishu_msg('{realName}，学号：{xh}，学院：{academy} '
                                    '发布的{scenes} \"{content}\"，触发了关键词\"{keyWord}\"'.format(realName=real_name,
                                                                                           xh=xh,
                                                                                           academy=academy,
                                                                                           scenes=scenes,
                                                                                           content=text,
                                                                                           keyWord=key_word.keyword))
                except Exception as e:
                    pass
    return content_state, comment_state, priority_delta
