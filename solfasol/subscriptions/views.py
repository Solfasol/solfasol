from django import forms
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from captcha.fields import ReCaptchaField
from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Subscription
        fields = ['name', 'email', 'address', 'type', 'phone', 'notes']
        widgets = {
            'type': forms.RadioSelect()
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
