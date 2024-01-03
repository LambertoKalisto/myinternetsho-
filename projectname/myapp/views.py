from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product, Cart, Order, Category
from django.views.generic import ListView
from django.db.models import Q
from .forms import OrderForm
from django.utils.text import slugify

def index(request):
    prod = Product.objects.order_by('-date')
    category = Category.objects.all()
    return render(request, 'myapp/index.html', {'prod': prod, 'category': category})

def about(request):
    return render(request, 'myapp/about.html')

class Search(ListView):

    template_name = 'myapp/index.html'
    context_object_name = 'prod'
    paginate_by = 8

    def get_queryset(self):
        search_query = self.request.GET.get('q', '').strip()
        return Product.objects.filter(Q(title__icontains=search_query))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context

class CategorySearch(ListView):

    template_name = 'myapp/index.html'
    context_object_name = 'prod'
    paginate_by = 8

    def get_queryset(self):
        category_query = self.request.GET.get('category', '').strip()

        queryset = Product.objects.filter(Q(category__title=category_query))

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['category'] = self.request.GET.get('category', '')
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

def order(request):
    error = ''
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            products_data = request.POST.getlist('products')
            for product_id in products_data:
                cart_item = Cart(product_id=product_id)
                cart_item.save()
                order.cart_items.add(cart_item)
            return render(request, 'myapp/order_success.html')
        else:
            print(form.errors)
            error = 'Не вірно заповнено форму'

    form = OrderForm()

    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'myapp/order.html', data)

