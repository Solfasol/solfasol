from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class SubscriptionType(models.Model):
    order = models.PositiveSmallIntegerField(default=1)
    title = models.CharField(max_length=50)
    amount = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=300, blank=True, null=True)
    payment_link = models.URLField()
    image = models.ImageField(upload_to='subscriptions/', blank=True, null=True)
    postal_address_required = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} - {self.amount} TL'

    class Meta:
        ordering = ('order',)


class Subscription(models.Model):
    name = models.CharField("Adınız, soyadınız", max_length=50)
    email = models.EmailField("E-posta adresiniz")
    address = models.CharField(
        "Posta adresiniz", blank=True, null=True, max_length=200,
        help_text="Dijital dışı abonelikler için gerekli"
    )
    type = models.ForeignKey(SubscriptionType, verbose_name="Abonelik tipi", blank=True, null=True, on_delete=models.SET_NULL)
    renewal = models.BooleanField(_('subscription status'), default=False,
        choices=((False, _('New subscription')),(True, _('Renewal')),)
    )
    phone = models.CharField("Telefon numaranız", max_length=20)
    notes = models.TextField("Eklemek istedikleriniz (Bize Notunuz)", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.type.postal_address_required and not self.address:
            raise ValidationError("Lütfen posta adresinizi belirtin.")

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
