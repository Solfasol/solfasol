# Generated by Django 3.0.7 on 2020-08-16 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_auto_20200815_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentcontributor',
            name='contribution_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.ContributionType', verbose_name='contribution type'),
        ),
    ]
