from django.db import models

# Create your models here.


class CaptureScreenTracking(models.Model):
    openId = models.CharField(db_index=True, default='', null=False, max_length=80, verbose_name='用户的openid',
                              help_text='用户的openid')
    pageUrl = models.TextField(null=True, blank=True, verbose_name='页面url')
    options = models.TextField(null=True, blank=True, verbose_name='页面参数')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='最后修改时间', help_text='最后修改时间')

    class Meta:
        verbose_name = '截屏事件'
        verbose_name_plural = verbose_name
