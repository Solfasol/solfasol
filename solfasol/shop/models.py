from django.db import models
from django.contrib.sessions.models import Session
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from slugify import slugify


class Category(models.Model):
    name = models.CharField(_('name'), max_length=50, blank=True, null=True)
    slug = models.SlugField(unique=True, editable=False)
    order = models.PositiveSmallIntegerField(_('order'), default=0, blank=True, null=True)

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(**kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('order',)


class Item(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(unique=True, editable=False)
    description = models.CharField(_('description'), max_length=250)
    tags = models.ManyToManyField('tag', verbose_name=_('tags'), blank=True)
    category = models.ForeignKey(
        Category, verbose_name=_('category'),
        on_delete=models.CASCADE
    )
    price = models.PositiveIntegerField()
    image = models.ImageField(_('image'), upload_to='shop/')
    available = models.BooleanField(_('available'), default=True)
    promoted = models.BooleanField(_('promoted'), default=False)
    added = models.DateTimeField(_('date'), auto_now_add=True)

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(**kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop_item_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('-added',)


class ItemAlternative(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    description = models.CharField(_('description'), max_length=250)
    price = models.DecimalField(_('price'), max_digits=6, decimal_places=2, blank=True, null=True)
    available = models.BooleanField(_('available'), default=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('alternative')
        verbose_name_plural = _('alternatives')


class Tag(models.Model):
    name = models.CharField(_('name'), max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


class Cart(models.Model):
    session = models.ForeignKey(
        Session,
        verbose_name=_('session'),
        on_delete=models.CASCADE,
    )
    items = models.ManyToManyField(Item, through='CartItem')

    def __str__(self):
        return self.session.id

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('session'), on_delete=models.CASCADE)
    item = models.ForeignKey(Item, verbose_name=_('item'), on_delete=models.CASCADE)
    added = models.DateTimeField(_('date'), auto_now_add=True)
    paid = models.BooleanField(_('paid'), default=False)

    def __str__(self):
        return '%s:%s' % (
            self.cart.__str__(),
            self.item.__str__()
        )


class Order(models.Model):
    name = models.CharField(_('Full name'), max_length=100)
    email = models.EmailField(_('Email'))
    gsm_number = models.CharField(_('Phone number'), max_length=20, blank=True, null=True)
    identity_number = models.CharField(_('Identity number'), max_length=11)
    address = models.CharField(_('Address'), max_length=200)
    city = models.CharField(_('City'), max_length=50)
    country = models.CharField(_('Country'), max_length=50)
    zipcode = models.CharField(_('Zip code'), max_length=6)

    notes = models.TextField(_('notes'), blank=True, null=True)

    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, verbose_name=_('cart'), blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
