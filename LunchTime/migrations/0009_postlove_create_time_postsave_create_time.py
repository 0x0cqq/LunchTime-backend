# Generated by Django 4.1.3 on 2023-05-14 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LunchTime', '0008_remove_postcomment_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='postlove',
            name='create_time',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='postsave',
            name='create_time',
            field=models.DateField(auto_now=True),
        ),
    ]