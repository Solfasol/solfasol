# Generated by Django 3.0.4 on 2020-05-24 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0018_contentsection_section_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentsectionimage',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
    ]