# Generated by Django 3.1.1 on 2020-09-17 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0008_auto_20200918_0006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='file_data',
        ),
        migrations.AddField(
            model_name='issue',
            name='page_data',
            field=models.TextField(blank=True, help_text='page data for creating pages remotely', null=True),
        ),
    ]
