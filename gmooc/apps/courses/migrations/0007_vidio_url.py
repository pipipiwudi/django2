# Generated by Django 2.0.7 on 2018-09-21 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='vidio',
            name='url',
            field=models.CharField(default='', max_length=200, verbose_name='访问地址'),
        ),
    ]
