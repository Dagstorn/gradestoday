# Generated by Django 3.1.3 on 2020-11-27 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handler', '0007_auto_20201127_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='positive',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.TextField(default=1, verbose_name='Комментарий'),
            preserve_default=False,
        ),
    ]
