# Generated by Django 3.1.2 on 2021-04-10 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0011_auto_20210405_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='type',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.SET_DEFAULT, to='subscriptions.subscriptiontype', verbose_name='Abonelik tipi'),
        ),
    ]