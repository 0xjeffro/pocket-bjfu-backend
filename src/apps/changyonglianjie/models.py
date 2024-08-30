from django.db import models

# Create your models here.


class ChangYongLianJie(models.Model):
    title = models.CharField(default='', null=False, max_length=20, verbose_name='网站名称', help_text='网站名称')
    desc = models.CharField(default='', null=False, max_length=30, verbose_name='网站描述', help_text='网站描述')
    url = models.CharField(default='', null=False, max_length=200, verbose_name='网站url', help_text='网站url')
    priority = models.IntegerField(default=0, null=False, verbose_name='优先级', help_text='优先级')

    class Meta:
        verbose_name = '常用链接'
        verbose_name_plural = verbose_name
