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
    request.session.set_expiry(1800)

    cart = request.session.get('cart', {})
    total_price = 0
    total_sum = 0
    for item in cart.values():
        item['total_price'] = item['price'] * item['quantity']
        total_price += item['total_price']
    total_sum = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'myapp/cart.html', {'cart': cart, 'total_sum': total_sum, 'total_price': total_price})

def cart_add(request, product_id):
    product = Product.objects.get(id=product_id)

    cart = request.session.get('cart', {})

    if str(product_id) not in cart:
        cart[product_id] = {
            'title': product.title,
            'price': product.price,
            'quantity': 1,
            'description': product.description,
            'image': {
                'url': product.image.url,
            },
        }
    else:
        cart[str(product_id)]['quantity'] += 1

    request.session['cart'] = cart

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})

    str_product_id = str(product_id)

    if str_product_id in cart:
        del cart[str_product_id]
        request.session['cart'] = cart

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def order(request):
    error = ''
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()

            cart = request.session.get('cart', {})

            for item_data in cart.values():
                product = Product.objects.get(
                    title=item_data['title'])
                cart_item = Cart.objects.create(
                    product=product,
                    price=item_data['price'],
                    quantity=item_data['quantity'],
                )
                order.cart_items.add(cart_item)

            request.session['cart'] = {}
            request.session.modified = True

            return render(request, 'myapp/order_success.html')
        else:
            print(form.errors)
            error = 'Не вірно заповнено форму'
    else:
        form = OrderForm()

    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'myapp/order.html', data)

