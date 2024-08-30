from django.db import models

# Create your models here.


class Notice(models.Model):
    priority = models.FloatField(default=0.0, null=False, blank=False, verbose_name='优先级')
    component = models.CharField(max_length=50, default='index', null=False, blank=False,
                                 verbose_name='组件', help_text='指定具体的一个NoticeBar')
    content = models.TextField(default='', null=False, blank=False, verbose_name='通知栏内容')

    xh_startswith = models.CharField(default='', max_length=20, null=False, blank=True,
                                     verbose_name='学号前缀', help_text='__startwith')

    color = models.CharField(default='#ed6a0c', max_length=20, null=False, blank=False, verbose_name='文字颜色')

    background = models.CharField(default='#fcefcf', max_length=20, null=False, blank=False, verbose_name='背景色')

    left_icon = models.CharField(default='', max_length=20, null=True, blank=True, verbose_name='左侧图标')

    delay = models.FloatField(default=0.5, null=False, blank=False, verbose_name='动画延迟')

    scrollable = models.BooleanField(default=True, null=False, blank=False, verbose_name='是否滚动')

    speed = models.IntegerField(default=32, null=False, blank=False, verbose_name='滚动速度')

    mode = models.CharField(default='None', max_length=20, null=False, blank=False,
                            choices=(('None', 'None'),
                                     ('link', 'link')), verbose_name='模式', help_text='link显示超链接箭头')

    to_type = models.CharField(default='None', max_length=20, null=False, blank=False,
                               choices=(('None', '不跳转'),
                                        ('miniprogram', '小程序'),
                                        ('url', '网页url')), verbose_name='跳转类型')
    to_url = models.TextField(default='', blank=True, null=True, help_text='跳转链接')
    show = models.BooleanField(default=True, help_text='是否生效')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = verbose_name