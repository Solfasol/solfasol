from django.db import models
from django.contrib.sessions.models import Session
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class Item(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(_('description'))
    price = models.PositiveIntegerField()
    image = models.ImageField(_('image'), upload_to='shop/')
    available = models.BooleanField(_('available'), default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop_item_detail', kwargs={'slug': self.slug})


class Cart(models.Model):
    session = models.ForeignKey(
        Session,
        verbose_name=_('session'),
        on_delete=models.CASCADE,
    )
    items = models.ManyToManyField(Item, through='CartItem')

    def __str__(self):
        return self.session.id


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('session'), on_delete=models.CASCADE)
    item = models.ForeignKey(Item, verbose_name=_('item'), on_delete=models.CASCADE)
    paid = models.BooleanField(_('paid'), default=False)

    def __str__(self):
        return '%s:%s' % (
            self.cart.__str__(),
            self.item.__str__()
        )
