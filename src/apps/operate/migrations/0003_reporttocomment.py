# Generated by Django 2.2 on 2021-06-22 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operate', '0002_auto_20210312_0012'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportToComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openId', models.CharField(db_index=True, help_text='举报用户的id', max_length=80, verbose_name='点赞用户的id')),
                ('contentId', models.IntegerField(db_index=True, help_text='被举报内容id', verbose_name='被举报内容id')),
                ('createTime', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('updateTime', models.DateTimeField(auto_now=True, help_text='最后修改时间', verbose_name='最后修改时间')),
            ],
        ),
    ]
