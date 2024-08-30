from django.db import models

# Create your models here.


class ColdUser(models.Model):
    xh = models.CharField(db_index=True, default='', null=True, max_length=30,
                          verbose_name='冷用户的学号', help_text='冷用户的学号')
    delta = models.IntegerField(default=-200, null=True, verbose_name='权重变量', help_text='权重变量，降权为负数')

    class Meta:
        verbose_name = '冷用户'
        verbose_name_plural = verbose_name


class ColdContent(models.Model):
    contentId = models.IntegerField(db_index=True, null=True,
                                    verbose_name='冷帖子id', help_text='冷帖子的id，只有评论或点赞、收藏过的用户能正常排名，对其它用户降权')
    page_number = models.IntegerField(default=10, verbose_name='限制页数', help_text='表示把该帖子限制在分页的第几页')

    class Meta:
        verbose_name = '冷帖子'
        verbose_name_plural = verbose_name


class KeyWords(models.Model):
    keyword = models.CharField(max_length=100, null=False,
                               verbose_name='屏蔽关键词', help_text='包含关键词的帖子会被处理')

    content_state = models.CharField(
                                     default='1', max_length=5, null=False, verbose_name='帖子触发后状态',
                                     choices=(('1', '正常'),
                                              ('0', '内容涉嫌违规，系统自动屏蔽'),
                                              # ('2', '该内容已被发布者删除'),
                                              ('3', '应相关方面要求，该内容已被删除'),
                                              ('4', '仅同班可见'),
                                              ('5', '仅同级同专业可见'),
                                              ('6', '仅同级同学院可见'),
                                              ('7', '仅作者自身可见')),
                                     help_text='控制内容显示状态，只有状态为正常的帖子可在列表中显示'
                                     )
    comment_state = models.CharField(default='1', max_length=5, null=False, verbose_name='评论触发后状态',
                                     choices=(('1', '正常'),
                                              ('0', '内容涉嫌违规，系统自动屏蔽'),
                                              ),
                                     help_text='内容状态 1-正常，0-隐藏，2-冷却')

    priority_delta = models.IntegerField(default=0, verbose_name='优先级变量', help_text='触发关键词后的优先级变量')

    if_notice = models.BooleanField(default=False, verbose_name='提醒', help_text='触发后是否推送到飞书')

    valid_time_to = models.DateTimeField(verbose_name='有效期至')

    remark = models.TextField(verbose_name='备注', blank=True, null=True)

    class Meta:
        verbose_name = '关键词策略'
        verbose_name_plural = verbose_name
