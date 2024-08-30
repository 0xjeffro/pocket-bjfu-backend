from django.db import models
# Create your models here.


class JiaoWuChuNews(models.Model):
    """
        教务处内容
        title: 标题 - primary_key
        time: 教务处网站上的发布时间
        url: 链接
        pic_url: 快照url
    """
    title = models.CharField(primary_key=True, default='', max_length=120, null=False, verbose_name='标题',
                             help_text='标题, primary_key')
    time = models.DateField(verbose_name='发布时间', help_text='教务处网站上的发布时间')

    url = models.CharField(default='', null=False, max_length=300, verbose_name='内容url', help_text='内容url')
    pic_url = models.CharField(default='', null=False, max_length=300, verbose_name='快照url', help_text='快照url')

    class Meta:
        verbose_name = '教务快讯'
        verbose_name_plural = verbose_name

