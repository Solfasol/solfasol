from django import forms
from django.shortcuts import render, redirect
from captcha.fields import ReCaptchaField
from .models import Subscription, SubscriptionType


class SubscriptionForm(forms.ModelForm):
    captcha = ReCaptchaField()
    type = forms.ModelChoiceField(
        queryset=SubscriptionType.objects,
        widget=forms.RadioSelect(),
        empty_label=None,
        label="Abonelik tipi",
    )

    class Meta:
        model = Subscription
        fields = ['name', 'email', 'address', 'type', 'renewal', 'phone', 'notes']
        widgets = {
            'type': forms.RadioSelect(),
            'renewal': forms.Select(),
        }


def subscribe(request):
    subscription = None
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save()
    else:
        form = SubscriptionForm()
    return render(request, 'subscriptions/subscription.html', {
        'form': form,
        'subscription_types': SubscriptionType.objects.filter(active=True),
        'subscription': subscription,
    })
