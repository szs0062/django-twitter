# Generated by Django 3.1.3 on 2022-02-16 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes_count',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
