# Generated by Django 2.0.7 on 2018-09-27 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavorite',
            name='fav_type',
            field=models.IntegerField(choices=[(1, '课程'), (2, '课程机构'), (3, '教师')], default=1, verbose_name='收藏类型'),
        ),
    ]
