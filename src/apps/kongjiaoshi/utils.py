from datetime import datetime, time


def get_day_of_week():
    """
    :return:
    1-7 代表今天是星期几
    """
    return datetime.now().isoweekday()


def get_current_jc():
    """
    根据当前时间返回当前的节次
    :return:
    0-5
    0：*-2节
    1：3-4节
    2：5节
    3：6-7节
    4：8-9节
    5：10-*节课
    """
    timetable = [
        time(9, 35),
        time(11, 25),
        time(12, 15),
        time(15, 5),
        time(16, 55)
    ]
    now = datetime.now()
    t_now = time(now.hour, now.minute)
    res = 0
    for key_time in timetable:
        if t_now < key_time:
            return res
        else:
            res += 1
    return res
