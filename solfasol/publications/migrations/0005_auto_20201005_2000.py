# Generated by Django 3.1.1 on 2020-10-05 17:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publications', '0004_publication_cover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='slug',
        ),
        migrations.AlterField(
            model_name='publication',
            name='editors',
            field=models.ManyToManyField(blank=True, related_name='managed_publications', to=settings.AUTH_USER_MODEL, verbose_name='editors'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='writers',
            field=models.ManyToManyField(blank=True, related_name='contributed_publications', to=settings.AUTH_USER_MODEL, verbose_name='writers'),
        ),
    ]