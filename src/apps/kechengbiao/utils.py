from django.conf import settings
import datetime


def get_days_of_week(currentWeek):
    """

    :param currentWeek:
    传入的currentWeek是一个[1, 最大周次]的正整数
    :return:
    返回一个list, 代表currentWeek的所有日期字符
    """
    currentWeek = int(currentWeek)
    days = []
    first_day_of_selected_week = settings.FIRST_WEEK_FIRST_DAY + datetime.timedelta(days=7*(currentWeek - 1))
    for i in range(7):
        item_day = first_day_of_selected_week + datetime.timedelta(days=i)
        s = str(item_day.month).zfill(2) + '/' + str(item_day.day).zfill(2)
        days.append(s)
    return days


def get_current_week():
    """
    根据setting中的FIRST_WEEK_FIRST_DAY 字段, 计算当前属于第几周
    :return:
    返回一个int
    """
    FIRST_WEEK_FIRST_DAY = settings.FIRST_WEEK_FIRST_DAY
    now = datetime.date.today()
    daydelta = now - FIRST_WEEK_FIRST_DAY
    if daydelta.days < 0:
        return 1
    elif int(daydelta.days/7) >= settings.MAX_WEEK:
        return settings.MAX_WEEK
    else:
        return int(daydelta.days / 7 + 1)
