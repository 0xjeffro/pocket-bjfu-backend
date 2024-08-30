from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    """
        用户基本信息
        openId -- 微信openId
    """

    openId = models.CharField(db_index=True, default='', null=False, max_length=80, verbose_name='用户的openid', help_text='用户的openid')
    xh = models.CharField(default='', null=True, max_length=30, verbose_name='学号', help_text='学号')
    pwd = models.CharField(default='', null=True, max_length=30, verbose_name='密码', help_text='密码')
    verifyType = models.CharField(default='0', null=False, max_length=10,
                                  choices=(
                                    ('0', '未验证'),
                                    ('1', '教务系统验证'),
                                    ('2', '新绿验证'),
                                    ('9', '超级管理员'),
                                    ('x', '黑名单用户')),
                                  verbose_name='验证类型', help_text='验证类型 0-未验证 1-教务系统验证 9-superuser x-黑名单用户 2-新绿验证')
    realName = models.CharField(default='', null=True, max_length=50, verbose_name='姓名',
                                help_text='新绿期间为验证时输入的姓名， 通过教务验证后为教务系统的真实姓名')
    academy = models.CharField(default='', null=True, max_length=100, verbose_name='学院名称', help_text='学院名称')
    acceptance_letter = models.CharField(default='', null=True, blank=True, max_length=300, verbose_name='录取通知书')
    last_active = models.DateTimeField(blank=True, null=True, verbose_name='最后活跃时间')

    ksh = models.CharField(default='', null=True, blank=True, max_length=40, verbose_name='考生号',
                           help_text='考生号，新绿验证时填写')
    sfzh = models.CharField(default='', null=True, blank=True, max_length=40, verbose_name='身份证号',
                            help_text='身份证号，新绿验证时填写')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class BlackUser(models.Model):
    openId = models.CharField(db_index=True, default='', null=False, max_length=80, verbose_name='用户的openid',
                              help_text='用户的openid')
    xh = models.CharField(db_index=True, default='', null=True, max_length=30, verbose_name='学号', help_text='学号')

    class Meta:
        verbose_name = '黑名单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.openId
