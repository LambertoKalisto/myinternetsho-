from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product, Cart, Order, Category
from django.views.generic import ListView
from django.db.models import Q
from .forms import OrderForm
from django.utils.text import slugify

# Визначаємо вид для головної сторінки
def index(request):
    # Отримуємо товари, впорядковані за датою
    prod = Product.objects.order_by('-date')
    # Отримуємо всі категорії
    category = Category.objects.all()
    # Відображаємо головну сторінку з даними про товари та категорії
    return render(request, 'myapp/index.html', {'prod': prod, 'category': category})

# Визначаємо вид для сторінки 'про нас'
def about(request):
    # Відображаємо сторінку 'про нас'
    return render(request, 'myapp/about.html')

# Визначаємо вид для пошуку продуктів
class Search(ListView):
    template_name = 'myapp/index.html'
    context_object_name = 'prod'
    paginate_by = 8

    def get_queryset(self):
        # Отримуємо пошуковий запит з параметра 'q' у GET-запиті
        search_query = self.request.GET.get('q', '').strip()
        # Фільтруємо товари за назвою, яка містить пошуковий запит
        return Product.objects.filter(Q(title__icontains=search_query))

    def get_context_data(self, *, object_list=None, **kwargs):
        # Отримуємо контекстні дані, додаємо пошуковий запит
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context

# Визначаємо вид для пошуку за категорією
class CategorySearch(ListView):
    template_name = 'myapp/index.html'
    context_object_name = 'prod'
    paginate_by = 8

    def get_queryset(self):
        # Отримуємо запит за категорією з параметра 'category' у GET-запиті
        category_query = self.request.GET.get('category', '').strip()
        # Фільтруємо товари за категорією
        queryset = Product.objects.filter(Q(category__title=category_query))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        # Отримуємо контекстні дані, додаємо пошуковий запит та категорію
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['category'] = self.request.GET.get('category', '')
        context['all_categories'] = Category.objects.all()
        return context


# Визначаємо вид для оновлення кошика
def update_cart(request, product_id, add=True):
    # Отримуємо об'єкт продукту або видаємо 404, якщо продукт не знайдено
    product = get_object_or_404(Product, id=product_id)

    # Отримуємо кошик з сесії або ініціалізуємо новий пустий кошик
    cart = request.session.get('cart', {})
    str_product_id = str(product_id)

    # Додаємо або оновлюємо елемент кошика
    if str_product_id not in cart:
        cart[str_product_id] = {
            'title': product.title,
            'price': product.price,
            'quantity': 1,
            'description': product.description,
            'image': {
                'url': product.image.url,
            },
        }
    else:
        if add:
            cart[str_product_id]['quantity'] += 1
        else:
            cart[str_product_id]['quantity'] -= 1
            # Видаляємо елемент кошика, якщо його кількість менше або дорівнює 0
            if cart[str_product_id]['quantity'] <= 0:
                del cart[str_product_id]

    # Зберігаємо оновлений кошик у сесії
    request.session['cart'] = cart


# Визначаємо вид для сторінки кошика
def cart(request):
    # Отримуємо кошик з сесії
    cart = request.session.get('cart', {})
    total_price = 0
    total_sum = 0

    # Обчислюємо загальну суму та вартість товарів у кошику
    for item in cart.values():
        item['total_price'] = item['price'] * item['quantity']
        total_price += item['total_price']

    # Альтернативний спосіб обчислення загальної вартості
    total_sum = sum(item['price'] * item['quantity'] for item in cart.values())

    # Відображаємо сторінку кошика з даними про товари та загальною вартістю
    return render(request, 'myapp/cart.html',
                  {'cart': cart, 'total_sum': round(total_sum, 2), 'total_price': total_price})

# Визначаємо вид для додавання товару до кошика
def cart_add(request, product_id):
    # Викликаємо функцію оновлення кошика для додавання товару
    update_cart(request, product_id)

    # Повертаємо користувача на попередню сторінку
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# Визначаємо вид для видалення товару з кошика
def cart_remove(request, product_id):
    # Викликаємо функцію оновлення кошика для видалення товару
    update_cart(request, product_id, add=False)

    # Повертаємо користувача на попередню сторінку
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Визначаємо вид для оформлення замовлення
def order(request):
    error = ''
    if request.method == 'POST':
        # Отримуємо дані форми з POST-запиту
        form = OrderForm(request.POST)
        if form.is_valid():
            # Зберігаємо дані замовлення, не зберігаючи його в базі даних
            order = form.save(commit=False)

            # Отримуємо кошик з сесії
            cart = request.session.get('cart', {})

            # Зберігаємо замовлення в базі даних
            order.save()

            # Додаємо товари з кошика до замовлення
            for item_data in cart.values():
                product = Product.objects.get(title=item_data['title'])
                cart_item = Cart.objects.create(
                    product=product,
                    price=item_data['price'],
                    quantity=item_data['quantity'],
                )
                order.cart_items.add(cart_item)

            # Очищаємо кошик у сесії
            request.session['cart'] = {}
            request.session.modified = True

            # Відображаємо сторінку успішного замовлення
            return render(request, 'myapp/order_success.html')
        else:
            # Виводимо помилки форми в консоль (для відладки)
            print(form.errors)
            error = 'Не вірно заповнено форму'
    else:
        # Ініціалізуємо форму для GET-запитів
        form = OrderForm()

    # Передаємо дані форми та помилку на сторінку замовлення
    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'myapp/order.html', data)




