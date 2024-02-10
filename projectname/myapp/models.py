from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify

class Category(models.Model):
    """
    Модель категорії для товарів.

    Attributes:
    - title (CharField): Назва категорії.
    - slug (SlugField): Слаг, унікальний ідентифікатор категорії.
    """

    title: models.CharField = models.CharField('Назва', max_length=50)
    slug: models.SlugField = models.SlugField('Slug', unique=True, max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Перевіряє, чи встановлено поле 'slug'. Якщо ні, генерує його на основі 'title'.
        Викликає базовий метод збереження.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Повертає рядкове представлення об'єкту - назва категорії.

        Returns:
        - str: Рядок - назва категорії.
        """
        return self.title

    class Meta:
        """
        Клас метаданих моделі Category.

        Attributes:
        - verbose_name (str): Описова назва одного об'єкту моделі.
        - verbose_name_plural (str): Описова назва багатьох об'єктів моделі.
        """
        verbose_name: str = 'Категорія'
        verbose_name_plural: str = 'Категорії'

class Product(models.Model):
    """
    Модель товару.

    Attributes:
    - title (CharField): Назва товару.
    - description (CharField): Опис товару.
    - price (FloatField): Ціна товару.
    - image (ImageField): Зображення товару.
    - date (DateTimeField): Дата публікації товару.
    - category (ForeignKey): Зовнішній ключ для зв'язку з категорією.
    """

    title: models.CharField = models.CharField('Назва', max_length=50)
    description: models.CharField = models.CharField('Опис товару', max_length=250)
    price: models.FloatField = models.FloatField('Ціна')
    image: models.ImageField = models.ImageField('Картинка', upload_to='images/')
    date: models.DateTimeField = models.DateTimeField('Дата публікації')
    category: models.ForeignKey[Category] = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self) -> str:
        """
        Повертає рядкове представлення об'єкту - назва товару.

        Returns:
        - str: Рядок - назва товару.
        """
        return self.title

    class Meta:
        """
        Клас метаданих моделі Product.

        Attributes:
        - verbose_name (str): Описова назва одного об'єкту моделі.
        - verbose_name_plural (str): Описова назва багатьох об'єктів моделі.
        """
        verbose_name: str = 'Товар'
        verbose_name_plural: str = 'Товари'

class Order(models.Model):
    """
    Модель замовлення.

    Attributes:
    - name (CharField): Ім'я замовника.
    - surname (CharField): Прізвище замовника.
    - shipping_address (CharField): Адреса доставки.
    - phone_number (CharField): Номер телефону замовника.
    - cart_items (ManyToManyField): Зв'язок з елементами кошика.

    """

    name: models.CharField = models.CharField("Ім'я", max_length=50)
    surname: models.CharField = models.CharField("Прізвище", max_length=50)
    adress: models.CharField = models.CharField("Адреса доставки", max_length=250)
    phonenumber: models.CharField = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                regex=r'^\+38?\d{10}$',
                message="Номер телефону повинен бути валідним."
            ),
        ],
    )

    def __str__(self) -> str:
        """
        Повертає рядкове представлення об'єкту - ім'я замовника.

        Returns:
        - str: Рядок - ім'я замовника.
        """
        return self.name

    # def __iter__(self):


    class Meta:
        """
        Клас метаданих моделі Order.

        Attributes:
        - verbose_name (str): Описова назва одного об'єкту моделі.
        - verbose_name_plural (str): Описова назва багатьох об'єктів моделі.
        """
        verbose_name: str = 'Замовлення'
        verbose_name_plural: str = 'Замовлення'

class Cart(models.Model):
    """
    Модель кошика покупок.

    Attributes:
    - product (ForeignKey): Зовнішній ключ для зв'язку з товаром.
    - quantity (PositiveSmallIntegerField): Кількість товару в кошику.
    - price (DecimalField): Ціна за одиницю товару.

    Methods:
    - sum(): Обчислює суму для елементу кошика.

    """

    product: models.ForeignKey[Product] = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity: models.PositiveSmallIntegerField = models.PositiveSmallIntegerField(default=0)
    price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    order: models.ForeignKey[Order] = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='cart_items')

    def sum(self) -> float:
        """
        Обчислює суму для елементу кошика.

        Returns:
        - float: Сума для елементу кошика.
        """
        return float(self.product.price * self.quantity)

    def __str__(self) -> str:
        """
        Повертає рядкове представлення об'єкту - рядок з кількість x назва товару.

        Returns:
        - str: Рядок вигляду "кількість x назва товару".
        """
        return f"{self.quantity} x {self.product.title}"

