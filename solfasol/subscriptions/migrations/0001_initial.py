# Generated by Django 3.0.4 on 2020-05-06 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Adınız, soyadınız')),
                ('email', models.EmailField(max_length=254, verbose_name='E-posta adresiniz')),
                ('address', models.CharField(blank=True, help_text='Dijital dışı abonelikler için gerekli', max_length=200, null=True, verbose_name='Posta adresiniz')),
                ('type', models.CharField(choices=[('yillik', "Yıllık abonelik - 100 TL (Solfasol'unuz her ay adresinize posta yoluyla ulaştırılır!)"), ('destekci', "Destekçi abonelik - 200 TL (Solfasol'un Ankara'nın farklı kesimlerine ulaşmasına destek olun!)"), ('dijital', "Dijital abonelik - 50 TL (Solfasol'unuz her ay elektronik posta kutunuzda!)"), ('yurtdisi', 'Yurtdışı abonelik - 200 TL (Uzaktayım demeyin, Solfasol dünyanın her yerine ulaşıyor!)')], max_length=10, verbose_name='Abonelik türü')),
                ('phone', models.CharField(max_length=20, verbose_name='Telefon numaranız')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Eklemek istedikleriniz (Bize Notunuz)')),
            ],
        ),
    ]