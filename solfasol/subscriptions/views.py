from django import forms
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from captcha.fields import ReCaptchaField
from .models import Subscription, SubscriptionType


class SubscriptionForm(forms.ModelForm):
    captcha = ReCaptchaField()
    sub_type = forms.ModelChoiceField(
        queryset=SubscriptionType.objects,
        widget=forms.RadioSelect(),
        empty_label=None,
        label="Abonelik tipi",
    )

    class Meta:
        model = Subscription
        fields = ['name', 'email', 'address', 'sub_type', 'renewal', 'phone', 'notes']
        widgets = {
            'sub_type': forms.RadioSelect(),
            'renewal': forms.Select(),
        }


def subscribe(request):
    subscription = None
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save()
            send_mail(
                'yeni abonelik',
                render_to_string('subscriptions/email.html', {
                    'subscription': subscription,
                }),
                from_email='Solfasol Abonelik <abonelik@solfasol.tv>',
                recipient_list=[subscription.email] + settings.DEFAULT_RECIPIENTS,
                fail_silently=True,
            )
    else:
        form = SubscriptionForm()
    return render(request, 'subscriptions/subscription.html', {
        'form': form,
        'subscription': subscription,
    })
