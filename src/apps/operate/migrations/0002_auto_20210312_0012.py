# Generated by Django 2.2 on 2021-03-12 00:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operate', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favtocontent',
            options={'verbose_name': '收藏帖子', 'verbose_name_plural': '收藏帖子'},
        ),
        migrations.AlterModelOptions(
            name='liketocomment',
            options={'verbose_name': '赞评论', 'verbose_name_plural': '赞评论'},
        ),
        migrations.AlterModelOptions(
            name='liketocontent',
            options={'verbose_name': '赞帖子', 'verbose_name_plural': '赞帖子'},
        ),
    ]
