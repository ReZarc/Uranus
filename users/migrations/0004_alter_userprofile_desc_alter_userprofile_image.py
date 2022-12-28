# Generated by Django 4.1.4 on 2022-12-25 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='desc',
            field=models.TextField(blank=True, default='这个人很懒，什么都没有写。', max_length=200, verbose_name='个人简介'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='images/default.png', upload_to='images/%Y/%m', verbose_name='用户头像'),
        ),
    ]