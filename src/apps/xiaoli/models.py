from django.db import models

# Create your models here.


class XiaoLi(models.Model):
    title = models.CharField(default='', null=False, max_length=20, verbose_name='图片标题', help_text='图片标题')
    img = models.CharField(default='', null=False, max_length=200, verbose_name='图片url', help_text='图片url')
    priority = models.IntegerField(default=0, null=False, verbose_name='优先级', help_text='优先级')

    class Meta:
        verbose_name = '校历'
        verbose_name_plural = verbose_name
