from django.db import models

# Create your models here.


class DefaultAD(models.Model):
    ad_text = models.CharField(default='', null=False, max_length=60, verbose_name='广告文案',
                               help_text='广告文案')
    ad_img = models.TextField(default='', verbose_name='广告配图', help_text='广告配图')

    tag_a_text = models.CharField(default='', null=True, blank=True, max_length=15, verbose_name='tagA文字', help_text='tagA文字')
    tag_a_color = models.CharField(default='#f85c23', null=True, blank=True, max_length=15, verbose_name='tagA颜色',
                                   help_text='tagA颜色')

    tag_b_text = models.CharField(default='', null=True, blank=True, max_length=15, verbose_name='tagB文字', help_text='tagB文字')
    tag_b_color = models.CharField(default='#f85c23', null=True, blank=True, max_length=15, verbose_name='tagB颜色',
                                   help_text='tagB颜色')

    button_text = models.CharField(default='', null=True, blank=True, max_length=20, verbose_name='引导按键文字')
    button_color = models.CharField(default='#5abe64', null=True, blank=True, max_length=15, verbose_name='引导按键颜色',
                                    help_text='引导按键颜色')

    feature_sex = models.CharField(default='all', null=True, max_length=20,
                                   choices=(('all', '性别不限'), ('male', '男'), ('female', '女')),
                                   verbose_name='广告能被该性别用户看到',
                                   help_text='广告能被该性别用户看到 all：全部 male：男性 female：女性')

    type = models.CharField(default='0', null=False, max_length=10,
                            choices=(('0', '复制淘口令'), ('1', '跳转小程序')),
                            verbose_name='广告类型',
                            help_text='0：复制淘口令  1：跳转小程序')

    additional_field_a = models.TextField(default='', null=True, blank=True, verbose_name='附加字段A', help_text='附加字段A')
    additional_field_b = models.TextField(default='', null=True, blank=True, verbose_name='附加字段B', help_text='附加字段B')

    rate = models.CharField(default='1/1000', max_length=50, null=False, verbose_name='频率限制',
                            help_text='频率限制，如60/10为60秒内显示不超过10次')
    valid_time = models.DateTimeField(verbose_name='有效时间至', help_text='广告在此期限前生效')

    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='最后修改时间', help_text='最后修改时间')

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name


class ADLog(models.Model):
    ad_id = models.IntegerField(null=False, verbose_name='广告id', help_text='广告id')
    openId = models.CharField(db_index=True, default='', null=False, max_length=80, verbose_name='用户的openid',
                              help_text='用户的openid')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='最后修改时间', help_text='最后修改时间')

    class Meta:
        verbose_name = '广告推送日志'
        verbose_name_plural = verbose_name
