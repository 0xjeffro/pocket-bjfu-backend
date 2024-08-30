from apps.users.models import UserProfile
from utils.idcardValidate import idcard_validate


def user_idcard_name_validate(name, idcard):
    """
    如果身份证号，不在2001-2004范围内， 禁止其进入
    验证身份证号和姓名的匹配，成功->return True, 否则return False
    """

    if int(idcard[6:10]) < 2001 or int(idcard[6:10]) > 2004:
        return False
    result = idcard_validate(idcard_number=idcard, name=name)
    return result
