from django.db import models

# Create your models here.


class Content(models.Model):
    openId = models.CharField(db_index=True, default='', null=False, max_length=80, verbose_name='作者的openId',
                              help_text='作者的openId')

    contentText = models.TextField(null=False, default='', blank=True, verbose_name='内容文字', help_text='内容文字')
    contentImg = models.TextField(null=True, default='', blank=True, verbose_name='内容配图url',
                                  help_text='内容配图url, url1|url2|url3|...')

    nLike = models.IntegerField(default=0, null=False, verbose_name='点赞数', help_text='点赞数')
    nComment = models.IntegerField(default=0, null=False, verbose_name='评论数', help_text='评论数')
    priority = models.FloatField(default=0.0, verbose_name='优先级', help_text='优先级')
    priority_delta = models.FloatField(default=0.0, verbose_name='优先级变量', help_text='优先级变量')
    setTop = models.BooleanField(default=False, null=True, blank=True, verbose_name='是否置顶', help_text='是否置顶')
    state = models.CharField(default='1', max_length=5, null=False, verbose_name='内容状态',
                             choices=(('1', '正常'),
                                      ('0', '内容涉嫌违规，系统自动屏蔽'),
                                      # ('2', '该内容已被发布者删除'),
                                      ('3', '应相关方面要求，该内容已被删除'),
                                      ('4', '仅同班可见'),
                                      ('5', '仅同级同专业可见'),
                                      ('6', '仅同级同学院可见'),
                                      ('7', '仅作者自身可见')),
                             help_text='控制内容显示状态，只有状态为正常的帖子可在列表中显示')

    decoration_url = models.TextField(null=True, default='', blank=True, verbose_name='挂件url', help_text='挂件url')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='最后修改时间', help_text='最后修改时间')

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = verbose_name


class ContentPriorityRuleForOpenId(models.Model):
    openId = models.CharField(primary_key=True, db_index=True, default='', max_length=80,
                              verbose_name='作者的openId',
                              help_text='作者的openId')
    priority_delta = models.FloatField(default=0.0, verbose_name='优先级变量', help_text='初始化优先级变量')

    class Meta:
        verbose_name = '优先级初始化规则(基于openId)'
        verbose_name_plural = verbose_name


class ContentPriorityRuleForXh(models.Model):
    xh = models.CharField(primary_key=True, db_index=True, default='', max_length=30,
                          verbose_name='学号', help_text='学号')
    priority_delta = models.FloatField(default=0.0, verbose_name='初始化优先级变量', help_text='初始化优先级变量')

    class Meta:
        verbose_name = '优先级初始化规则(基于学号)'
        verbose_name_plural = verbose_name
