from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product, Cart
from django.views.generic import ListView
from django.db.models import Q

def index(request):
    prod = Product.objects.order_by('-date')
    return render(request, 'myapp/index.html', {'prod': prod})

def about(request):
    return render(request, 'myapp/about.html')

class Search(ListView):

    template_name = 'myapp/index.html'
    context_object_name = 'prod'
    paginate_by = 5

    def get_queryset(self):
        search_query = self.request.GET.get('q', '').strip()
        return Product.objects.filter(Q(title__icontains=search_query))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context

def cart(request):
    cart = Cart.objects.all()
    total_sum = 0
    total_quantity = 0
    for el in cart:
        total_sum += el.sum()
    return render(request, 'myapp/cart.html', {'cart': cart, 'total_sum': total_sum})

def cart_add(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.filter(product=product)

    if not cart.exists():
        Cart.objects.create(product=product, quantity=1)
    else:
        cart = cart.first()
        cart.quantity += 1
        cart.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def cart_remove(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])



