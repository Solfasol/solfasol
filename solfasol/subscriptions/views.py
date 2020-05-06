from django import forms
from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'email', 'address', 'type', 'phone', 'notes']
        widgets = {
            'type': forms.RadioSelect()
        }

def subscribe(request):
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
                fail_silently=False,
            )
            messages.success(request, 'Thank you for your support! We will contact you soon!')
    else:
        form = SubscriptionForm()
    return render(request, 'subscriptions/form.html', {
        'form': form,
    })
