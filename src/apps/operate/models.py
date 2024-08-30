from django.db import models

# Create your models here.


class LikeToContent(models.Model):

    openId = models.CharField(db_index=True, null=False, max_length=80, verbose_name='点赞用户的id',
                              help_text='点赞用户的id')
    contentId = models.IntegerField(null=False, verbose_name='被点赞内容id',
                                    help_text='被点赞内容id')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='最后修改时间', help_text='最后修改时间')

    class Meta:
        unique_together = ('openId', 'contentId')
        verbose_name = '赞帖子'
        verbose_name_plural = verbose_name


class FavToContent(models.Model):
    """
        收藏-内容卡片
    """
    openId = models.CharField(db_index=True, null=False, max_length=80, verbose_name='收藏用户的id',
                              help_text='收藏用户的id')
    contentId = models.IntegerField(null=False, verbose_name='被收藏内容id',
                                    help_text='被收藏内容id')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='最后修改时间', help_text='最后修改时间')

    class Meta:
        unique_together = ('openId', 'contentId')
        verbose_name = '收藏帖子'
        verbose_name_plural = verbose_name


class LikeToComment(models.Model):
    """
        点赞-评论
    """
    openId = models.CharField(db_index=True, null=False, max_length=80, verbose_name='点赞用户的id',
                              help_text='点赞用户的id')
    commentId = models.IntegerField(null=False, verbose_name='被点赞评论id',
                                    help_text='被点赞评论id')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='最后修改时间', help_text='最后修改时间')

    class Meta:
        unique_together = ('openId', 'commentId')
        verbose_name = '赞评论'
        verbose_name_plural = verbose_name


class ReportToContent(models.Model):
    """
        用户举报-内容
    """
    openId = models.CharField(db_index=True, null=False, max_length=80, verbose_name='举报用户的openId',
                              help_text='举报用户的openId')
    contentId = models.IntegerField(db_index=True, null=False, verbose_name='被举报内容id',
                                    help_text='被举报内容id')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='最后修改时间', help_text='最后修改时间')

    class Meta:
        verbose_name = '举报内容'
        verbose_name_plural = verbose_name