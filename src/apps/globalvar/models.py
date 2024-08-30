from django.db import models

# Create your models here.


class GlobalVar(models.Model):
    key = models.CharField(primary_key=True, default='', null=False, max_length=100, verbose_name='键')
    value = models.TextField(default='', verbose_name='值')
    help_text = models.TextField(default='', blank=True, verbose_name='备注', help_text='备注')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='最后修改时间', help_text='最后修改时间')

    class Meta:
        verbose_name = '全局变量'
        verbose_name_plural = verbose_name
