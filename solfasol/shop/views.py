from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Item, Cart, CartItem


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
