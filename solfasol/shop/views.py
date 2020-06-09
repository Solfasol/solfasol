import json
from base64 import b64decode
from datetime import date
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.contrib import messages
from django import forms
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
import iyzipay
from .fields import CreditCardNumberField, VerificationValueField
from .models import Item, Cart, CartItem, Order


API_PARAMS = {
    'api_key': settings.IYZICO_API_KEY,
    'secret_key': settings.IYZICO_SECRET_KEY,
    'base_url': 'api.iyzipay.com'
}

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
    return redirect(request.GET.get('next') or 'shop_item_list')


class PaymentForm(forms.ModelForm):
    card_holder_name = forms.CharField(label=_('Card holder name'))
    card_number = CreditCardNumberField(label=_('Card number'))
    expiry_month = forms.ChoiceField(choices=[(x, '%02d' % x) for x in range(1, 13)])
    expiry_year = forms.ChoiceField(choices=[(x, x) for x in range(YEAR, YEAR + 15)])
    cvc = VerificationValueField(label=_('CVC'))
    secure3d = forms.BooleanField(label=_('3D Secure'), initial=True)

    class Meta:
        model = Order
        exclude = []


def payment_form(request):
    cart = Item.objects.filter(id__in=request.session.get('cart', []))
    price_total = sum([item.price for item in cart])
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_card = {
                'cardHolderName': form.cleaned_data['card_holder_name'],
                'cardNumber': form.cleaned_data['card_number'],
                'expireMonth': form.cleaned_data['expiry_month'],
                'expireYear': form.cleaned_data['expiry_year'],
                'cvc': form.cleaned_data['cvc'],
            }
            order = form.save()
            buyer = {
                'id': str(order.id),
                'name': ' '.join(order.name.split()[:-1]),
                'surname': order.name.split()[-1],
                'gsmNumber': order.gsm_number,
                'email': order.email,
                'identityNumber': order.identity_number,
                'registrationAddress': order.address,
                'ip': request.META.get(
                    'HTTP_X_FORWARDED_FOR',
                    request.META.get(
                        'REMOTE_ADDR', '')
                ).split(',')[0].strip(),
                'city': order.city,
                'country': order.country,
                'zipCode': order.zipcode,
            }
            address = {
                'contactName': order.name,
                'city':  order.city,
                'country': order.country,
                'address': order.address,
                'zipCode': order.zipcode,
            }
            basket_items = [
                {
                    'id': '12345',
                    'name': 'Gazete',
                    'category1': 'Gazete',
                    # 'category2': 'Accessories',
                    'itemType': 'PHYSICAL',
                    'price': '1'
                },
            ]
            req = {
                'locale': 'tr',
                'conversationId': str(order.id),
                'price': price_total,
                'paidPrice': price_total,
                'currency': 'TRY',
                'installment': '1',
                'paymentGroup': 'PRODUCT',  # PRODUCT, LISTING, SUBSCRIPTION, OTHER
                'paymentCard': payment_card,
                'buyer': buyer,
                'shippingAddress': address,
                'billingAddress': address,
                'basketItems': basket_items,
            }
            if form.cleaned_data['secure3d']:
                req.update({
                    'callbackUrl': '%s%s' % (
                        settings.SITE_BASE_URL,
                        reverse('shop_3ds_callback')
                    ),
                })
                three_d_s_initialize = iyzipay.ThreedsInitialize()
                r = three_d_s_initialize.create(req, API_PARAMS)
                if r.status == 200:
                    response = json.loads(r.read())
                    if response['status'] == 'success':
                        print(response['threeDSHtmlContent'])
                        return render(request, 'shop/3ds_form.html', {
                            '3ds_bank_form': b64decode(response['threeDSHtmlContent']).decode('utf-8'),
                        })
            else:
                payment = iyzipay.Payment().create(req, API_PARAMS)

    else:
        form = PaymentForm()
    return render(request, 'shop/payment_form.html', {
        'form': form,
        'cart': cart,
        'price_total': price_total,
    })


@csrf_exempt
def callback_3d(request):
    if request.POST.get('status') == 'success':
        if request.POST.get('mdStatus') == '1':
            params = {
                'locale': 'tr',
                'paymentId': request.POST.get('paymentId'),
                'conversationId': request.POST.get('conversationId'),
            }
            if request.POST.get('conversationData'):
                params.update({
                    'conversationData': request.POST.get('conversationData'),
                })
            payment = iyzipay.ThreedsPayment().create(params, API_PARAMS)
            return render(request, 'shop/test.html', {
                'payment_params': payment.read(),
            })

"""
b'{"status":"success","locale":"tr","systemTime":1591653859298,"conversationId":"7","price":1.00000000,"paidPrice":1.00000000,"installment":1,"paymentId":"843442341","fraudStatus":1,"merchantCommissionRate":0E-8,"merchantCommissionRateAmount":0E-8,"iyziCommissionRateAmount":0.02290000,"iyziCommissionFee":0.25000000,"cardType":"CREDIT_CARD","cardAssociation":"VISA","cardFamily":"Maximum","binNumber":"454360","lastFourDigits":"5485","currency":"TRY","itemTransactions":[{"itemId":"12345","paymentTransactionId":"703942696","transactionStatus":2,"price":1.00000000,"paidPrice":1.00000000,"merchantCommissionRate":0E-8,"merchantCommissionRateAmount":0E-8,"iyziCommissionRateAmount":0.02290000,"iyziCommissionFee":0.25000000,"blockageRate":0E-8,"blockageRateAmountMerchant":0E-8,"blockageRateAmountSubMerchant":0,"blockageResolvedDate":"2020-06-12 00:00:00","subMerchantPrice":0,"subMerchantPayoutRate":0E-8,"subMerchantPayoutAmount":0,"merchantPayoutAmount":0.72710000,"convertedPayout":{"paidPrice":1.00000000,"iyziCommissionRateAmount":0.02290000,"iyziCommissionFee":0.25000000,"blockageRateAmountMerchant":0E-8,"blockageRateAmountSubMerchant":0E-8,"subMerchantPayoutAmount":0E-8,"merchantPayoutAmount":0.72710000,"iyziConversionRate":0,"iyziConversionRateAmount":0,"currency":"TRY"}}],"authCode":"426031","phase":"AUTH","mdStatus":1,"hostReference":"016101767396"}'
"""