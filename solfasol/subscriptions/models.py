from django.db import models
from django.utils.translation import ugettext_lazy as _


class Subscription(models.Model):
    name = models.CharField("Adınız, soyadınız", max_length=50)
    email = models.EmailField("E-posta adresiniz")
    address = models.CharField(
        "Posta adresiniz", blank=True, null=True, max_length=200,
        help_text="Dijital dışı abonelikler için gerekli"
    )
    type = models.CharField("Abonelik türü", max_length=10, default='destekci', choices=(
        ('dijital', "Dijital abonelik - 50 TL (Solfasol'unuz her ay elektronik posta kutunuzda!)"),
        ('yillik', "Yıllık abonelik - 100 TL (Solfasol'unuz her ay adresinize posta yoluyla ulaştırılır!)"),
        ('destekci', "Destekçi abonelik - 200 TL (Solfasol'un Ankara'nın farklı kesimlerine ulaşmasına destek olun! "
                     "Ayrıca Solfasol Ankara Gezilerinde misafirimiz olun."),
        ('yurtdisi', "Yurtdışı abonelik - 200 TL (Uzaktayım demeyin, Solfasol dünyanın her yerine ulaşıyor!)"),
    ))
    phone = models.CharField("Telefon numaranız", max_length=20)
    notes = models.TextField("Eklemek istedikleriniz (Bize Notunuz)", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
