# Generated by Django 4.1.3 on 2023-05-03 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LunchTime', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set(),
        ),
    ]
