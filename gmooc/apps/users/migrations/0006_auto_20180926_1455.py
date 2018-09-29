# Generated by Django 2.0.7 on 2018-09-26 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180918_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '找回'), ('update', '修改邮箱')], default='register', max_length=10, verbose_name='验证类型'),
        ),
    ]
