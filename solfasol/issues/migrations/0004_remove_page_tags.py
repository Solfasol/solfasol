# Generated by Django 3.0.7 on 2020-08-16 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0003_auto_20200813_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='tags',
        ),
    ]
