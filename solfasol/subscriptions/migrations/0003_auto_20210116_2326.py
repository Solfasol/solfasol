# Generated by Django 3.1.2 on 2021-01-16 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_subscription_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='type',
            field=models.CharField(choices=[('dijital', 'Dijital abonelik - 100 TL'), ('yillik', 'Yıllık abonelik - 150 TL'), ('destekci', 'Destekçi abonelik - 300 TL'), ('yurtdisi', 'Yurtdışı abonelik - 300 TL'), ('duble', 'Duble Destekçi abonelik - 600 TL'), ('yasasin', 'Yaşasın SOLFASOL! aboneliği - 1000 TL')], default='destekci', max_length=10, verbose_name='Abonelik türü'),
        ),
    ]
