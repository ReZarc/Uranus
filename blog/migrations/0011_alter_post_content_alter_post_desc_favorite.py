# Generated by Django 4.1.4 on 2023-01-06 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0010_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, default='', max_length=2000, verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='post',
            name='desc',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='文章描述'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='blog.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '收藏',
                'verbose_name_plural': '收藏',
            },
        ),
    ]
