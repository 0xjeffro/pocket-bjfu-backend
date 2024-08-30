from apps.users.models import BlackUser
from utils.FeiShuMessage import send_feishu_msg
from django.db.models import Q


def is_black_user(user):
    q = BlackUser.objects.filter(Q(openId=user.openId) | Q(xh=user.xh))
    if len(q) == 0:
        return False
    else:
        return True
