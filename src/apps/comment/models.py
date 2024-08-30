from django.db import models

# Create your models here.


class Comment(models.Model):
    openId = models.CharField(db_index=True, default='', null=False, max_length=80, verbose_name='作者的openId',
                              help_text='作者的openId')
    commentText = models.TextField(null=False, default='', blank=True, verbose_name='内容文字', help_text='内容文字')

    nLike = models.IntegerField(default=0, null=False, verbose_name='点赞数', help_text='点赞数')

    deep = models.IntegerField(default=1, null=False, verbose_name='评论级数', help_text='评论级数 1-一级评论，2-二级评论')

    reply = models.IntegerField(default=-1, null=True, verbose_name='回复的commentId',
                                help_text='回复的commentId,仅对二级评论生效, 否则为-1')
    contentId = models.IntegerField(null=False, db_index=True, verbose_name='所属的帖子id', help_text='评论及回复所属的内容的id')
    commentId = models.IntegerField(default=-1, db_index=True, verbose_name='父评论的id',
                                    help_text='二级评论所属的一级评论的id')
    state = models.CharField(default='1', max_length=5, null=False, verbose_name='内容状态',
                             choices=(('1', '正常'),
                                      ('0', '内容涉嫌违规，系统自动屏蔽'),
                                      ),
                             help_text='内容状态 1-正常，0-隐藏，2-冷却')

    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='最后修改时间', help_text='最后修改时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
