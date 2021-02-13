from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class SubscriptionType(models.Model):
    title = models.CharField(max_length=50)
    amount = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True, null=True)
    payment_link = models.URLField()
    image = models.ImageField(upload_to='subscriptions/', blank=True, null=True)
    postal_address_required = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    name = models.CharField("Adınız, soyadınız", max_length=50)
    email = models.EmailField("E-posta adresiniz")
    address = models.CharField(
        "Posta adresiniz", blank=True, null=True, max_length=200,
        help_text="Dijital dışı abonelikler için gerekli"
    )
    sub_type = models.ForeignKey(SubscriptionType, blank=True, null=True, on_delete=models.SET_NULL)
    type = models.CharField("Abonelik türü", max_length=10, default='destekci', choices=(
        ('dijital', "Dijital abonelik - 100 TL"),
        ('yillik', "Normal abonelik - 150 TL"),
        ('destekci', "Destekçi abonelik - 300 TL"),
        ('yurtdisi', "Yurtdışı abonelik - 300 TL"),
        ('duble', "Çifte Destekçi abonelik - 600 TL"),
        ('yasasin', "Yaşasın SOLFASOL! aboneliği - 1000 TL"),
    ))
    renewal = models.BooleanField(_('subscription status'), default=False,
        choices=((False, _('New subscription')),(True, _('Renewal')),)
    )
    phone = models.CharField("Telefon numaranız", max_length=20)
    notes = models.TextField("Eklemek istedikleriniz (Bize Notunuz)", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.sub_type.postal_address_required and not self.address:
            raise ValidationError("Lütfen posta adresinizi belirtin.")

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
