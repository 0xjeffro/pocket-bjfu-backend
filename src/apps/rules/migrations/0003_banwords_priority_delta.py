# Generated by Django 2.2 on 2021-12-22 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0002_banwords'),
    ]

    operations = [
        migrations.AddField(
            model_name='banwords',
            name='priority_delta',
            field=models.IntegerField(default=0, help_text='触发关键词后的优先级变量', verbose_name='优先级变量'),
        ),
    ]
