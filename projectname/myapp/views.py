from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product, Cart, Order, Category
from django.views.generic import ListView
from django.db.models import Q
from .forms import OrderForm
from django.utils.text import slugify
from .cart import CartSession

# Define view for the main page
def index(request):
    # Get products ordered by date
    prod = Product.objects.order_by('-date')
    # Get all categories
    category = Category.objects.all()
    # Display the main page with product and category data
    return render(request, 'myapp/index.html', {'prod': prod, 'category': category})

# Define view for the 'about us' page
def about(request):
    # Display the 'about us' page
    return render(request, 'myapp/about.html')

# Define view for product search
class Search(ListView):
    template_name = 'myapp/index.html'
    context_object_name = 'prod'
    paginate_by = 8

    def get_queryset(self):
        # Get search query from 'q' parameter in GET request
        search_query = self.request.GET.get('q', '').strip()
        # Filter products by title containing search query
        return Product.objects.filter(Q(title__icontains=search_query))

    def get_context_data(self, *, object_list=None, **kwargs):
        # Get context data, add search query
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context

# Define view for category search
class CategorySearch(ListView):
    template_name = 'myapp/index.html'
    context_object_name = 'prod'
    paginate_by = 8

    def get_queryset(self):
        # Get category query from 'category' parameter in GET request
        category_query = self.request.GET.get('category', '').strip()
        # Filter products by category
        queryset = Product.objects.filter(Q(category__title=category_query))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        # Get context data, add search query and category
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['category'] = self.request.GET.get('category', '')
        context['all_categories'] = Category.objects.all()
        return context

# Define view for updating the cart
def update_cart(request, product_id, add=True):
    # Get product object or return 404 if product not found
    product = get_object_or_404(Product, id=product_id)

    # Get cart from session or initialize a new empty cart
    cart = CartSession(request)
    if add:
        cart.add(product)
    else:
        cart.remove(product)

# Define view for the cart page
def cart(request):
    # Get cart from session
    cart = CartSession(request)

    return render(request, 'myapp/cart.html',
                  {'cart': cart, 'total_sum': len(cart), 'total_price': cart.get_total_price()})

# Define view for adding a product to the cart
def cart_add(request, product_id):
    # Call update_cart function to add the product
    update_cart(request, product_id)

    # Redirect user to the previous page
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# Define view for removing a product from the cart
def cart_remove(request, product_id):
    # Call update_cart function to remove the product
    update_cart(request, product_id, add=False)

    # Redirect user to the previous page
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# Define view for placing an order
def order(request):
    error = ''
    if request.method == 'POST':
        # Get form data from POST request
        form = OrderForm(request.POST)
        if form.is_valid():
            # Save order data without saving it to the database
            order = form.save(commit=False)

            # Get cart from session
            cart = CartSession(request)

            # Save order to the database
            order.save()

            # Add cart items to the order
            for item_data in cart:
                cart_item = Cart.objects.create(
                    product=item_data['product'],
                    price=item_data['price'],
                    quantity=item_data['quantity'],
                    order=order,
                )

            # Clear the cart in the session
            cart.clear()

            # Display the order success page
            return render(request, 'myapp/order_success.html')
        else:
            # Print form errors to console (for debugging)
            print(form.errors)
            error = 'Не вірно заповнено форму'
    else:
        # Initialize form for GET requests
        form = OrderForm()

    # Pass form data and error to the order page
    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'myapp/order.html', data)