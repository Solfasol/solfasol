from datetime import date
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.conf import settings
from django import forms
from django.utils.translation import ugettext as _
import iyzipay
from .fields import CreditCardNumberField, ExpiryDateField, VerificationValueField
from .models import Item, Cart, CartItem


YEAR = date.today().year


class ItemListView(ListView):
    model = Item
    context_object_name = 'item_list'

    def get_queryset(self):
        qs = super().get_queryset().filter(available=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'cart': Item.objects.filter(id__in=self.request.session.get('cart', [])),
        })
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = 'shop/item_detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'other_items': Item.objects.filter(available=True).exclude(id=self.get_object().id),
            'cart': Item.objects.filter(id__in=self.request.session.get('cart', [])),
        })
        return context


def cart_add(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart = request.session.get('cart', [])
    cart.append(item.id)
    request.session['cart'] = cart
    return redirect('shop_item_list')


def cart_remove(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart = request.session.get('cart', [])
    try:
        cart.remove(item.id)
    except ValueError:
        pass
    request.session['cart'] = cart
    return redirect('shop_item_list')


class PaymentForm(forms.Form):
    name = forms.CharField(label=_('Full name'))
    email = forms.EmailField(label=_('Email'))
    gsm_number = forms.CharField(label=_('Phone number'), required=False)
    identity_number = forms.CharField(label=_('Identity number'))
    address = forms.CharField(label=_('Address'))
    city = forms.CharField(label=_('City'))
    country = forms.CharField(label=_('Country'))
    zipcode = forms.CharField(label=_('Zip code'))

    card_holder_name = forms.CharField(label=_('Card holder name'))
    card_number = CreditCardNumberField(label=_('Card number'))
    expiry_date = ExpiryDateField(label=_('Expiry date'))
    expiry_month = forms.ChoiceField(choices=[(x, '%02d' % x) for x in range(1, 13)])
    expiry_year = forms.ChoiceField(choices=[(x, x) for x in range(YEAR, YEAR + 15)])
    cvc = VerificationValueField(label=_('CVC'))
    secure3d = forms.BooleanField(label=_('3D Secure'), initial=True)


def payment_form(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = PaymentForm()
    return render(request, 'shop/payment_form.html', {
        'form': form,
    })


def checkout(request):
    options = {
        'api_key': settings.IYZICO_API_KEY,
        'secret_key': settings.IYZICO_SECRET_KEY,
        'base_url': 'api.iyzipay.com'
    }
    payment_card = {
        'cardHolderName': 'HAZIM ONUR MAT',
        'cardNumber': '4543609200705485',
        'expireMonth': '10',
        'expireYear': '2021',
        'cvc': '372',
        'registerCard': '0'
    }
    buyer = {
        'id': 'omat',
        'name': 'Onur',
        'surname': 'Mat',
        'gsmNumber': '+905355568220',
        'email': 'onurmatik@gmail.com',
        'identityNumber': '74300864791',
        'registrationAddress': 'Buklum sok. 44/4 Cankaya',
        'ip': '85.34.78.112',
        'city': 'Ankara',
        'country': 'Turkey',
        'zipCode': '06600'
    }

    address = {
        'contactName': 'Onur Mat',
        'city': 'Ankara',
        'country': 'Turkey',
        'address': 'Buklum sok. 44/4 Cankaya',
        'zipCode': '06600'
    }

    basket_items = [
        {
            'id': '12345',
            'name': 'Gazete',
            'category1': 'Gazete',
            #'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': '1'
        },
    ]

    req = {
        'locale': 'tr',
        'conversationId': '123456789',
        'price': '1',
        'paidPrice': '1',
        'currency': 'TRY',
        'installment': '1',
        'basketId': 'B67832',
        'paymentChannel': 'WEB',
        'paymentGroup': 'PRODUCT',
        'paymentCard': payment_card,
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items,
        'callbackUrl': '',
    }

    payment = iyzipay.Payment().create(req, options)

    three_d_s_initialize = iyzipay.ThreeDSInitialize()
    three_d_s_initialize_response = three_d_s_initialize.create(request, options)

    return render(request, 'shop/3ds_form.html', {
        '3ds_bank_form': three_d_s_initialize_response['threedsHtmlContent'],
    })


def callback_3d(request):
    payment_id = request.GET.get('paymentId')
