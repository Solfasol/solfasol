from django.views.generic import ListView, DetailView
from .models import Item, Cart


class ItemListView(ListView):
    model = Item
    context_object_name = 'item_list'

    def get_queryset(self):
        qs = super().get_queryset().filter(available=True)
        return qs


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
        })
        return context
