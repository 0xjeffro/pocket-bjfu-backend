# Generated by Django 2.2 on 2021-05-24 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('behaviortracking', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='capturescreentracking',
            options={'verbose_name': '截屏事件', 'verbose_name_plural': '截屏事件'},
        ),
        migrations.AddField(
            model_name='capturescreentracking',
            name='options',
            field=models.TextField(blank=True, null=True, verbose_name='页面参数'),
        ),
    ]
