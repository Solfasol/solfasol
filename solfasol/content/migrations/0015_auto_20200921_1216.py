# Generated by Django 3.1.1 on 2020-09-21 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0009_auto_20200918_0020'),
        ('content', '0014_auto_20200921_1103'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seriescontributor',
            options={'verbose_name': 'series contributor', 'verbose_name_plural': 'series contributors'},
        ),
        migrations.AddField(
            model_name='series',
            name='issue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='issues.issue', verbose_name='issue'),
        ),
    ]