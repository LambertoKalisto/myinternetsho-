from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify

class Category(models.Model):
    """
    Model categories for products.

    Attributes:
    - title (CharField): Category name.
    - slug (SlugField): Slug, a unique category identifier.
    """

    title: models.CharField = models.CharField('Назва', max_length=50)
    slug: models.SlugField = models.SlugField('Slug', unique=True, max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Checks whether the 'slug' field is inserted. However, it generates it based on 'title'.
        Viklika is a basic saving method.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Turns the row of representations of the object - the name of the category.

        Returns:
        - str: Row - category name.
        """
        return self.title

    class Meta:
        """
        Model metadata class Category.

        Attributes:
        - verbose_name (str): Describes the name of one model object.
        - verbose_name_plural (str): Descriptive names of many objects in the model.
        """
        verbose_name: str = 'Категорія'
        verbose_name_plural: str = 'Категорії'

class Product(models.Model):
    """
    Product model.

    Attributes:
    - title (CharField): The name of the product.
    - description (CharField): Description of the product.
    - price (FloatField): Product price.
    - image (ImageField): Image of the product.
    - date (DateTimeField): Date of publication of the product.
    - category (ForeignKey): Foreign key for linking with the category.
    """

    title: models.CharField = models.CharField('Назва', max_length=50)
    description: models.CharField = models.CharField('Опис товару', max_length=250)
    price: models.FloatField = models.FloatField('Ціна')
    image: models.ImageField = models.ImageField('Картинка', upload_to='images/')
    date: models.DateTimeField = models.DateTimeField('Дата публікації')
    category: models.ForeignKey[Category] = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self) -> str:
        """
        Turns around the presentation of the object - the name of the product.

        Returns:
        - str: Row - the name of the product.
        """
        return self.title

    class Meta:
        """
        Product model metadata class.

        Attributes:
        - verbose_name (str): Describes the name of one model object.
        - verbose_name_plural (str): Descriptive names of many objects in the model.
        """
        verbose_name: str = 'Товар'
        verbose_name_plural: str = 'Товари'

class Order(models.Model):
    """
    The contract model.

    Attributes:
    - name (CharField): Name of the deputy.
    - surname (CharField): Nickname of the deputy.
    - shipping_address (CharField): Shipping addresses.
    - phone_number (CharField): Phone number of the deputy.

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
        Turns the row of representations to the object - the name of the deputy.

        Returns:
        - str: Row - name of the deputy.
        """
        return self.name

    # def __iter__(self):


    class Meta:
        """
        Metadata class of the Order model.

        Attributes:
        - verbose_name (str): Describes the name of one model object.
        - verbose_name_plural (str): Descriptive names of many objects in the model.
        """
        verbose_name: str = 'Замовлення'
        verbose_name_plural: str = 'Замовлення'

class Cart(models.Model):
    """
    Shopping cart model.

    Attributes:
    - product (ForeignKey): Foreign key for linking with the product.
    - quantity (PositiveSmallIntegerField): Quantity of product in a box.
    - price (DecimalField): Price per item.
    - order (ForeignKey): Foreign key for linking with the Order.

    Methods:
    - sum(): Calculate the sum for the cat element.

    """

    product: models.ForeignKey[Product] = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity: models.PositiveSmallIntegerField = models.PositiveSmallIntegerField(default=0)
    price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    order: models.ForeignKey[Order] = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='cart_items')

    def sum(self) -> float:
        """
        Calculate the amount for the cat element.

        Returns:
        - float: Sum for the cat element.
        """
        return float(self.product.price * self.quantity)

    def __str__(self) -> str:
        """
        Turns the row presented to the object - row with quantity x name of the product.

        Returns:
        - str: The row looks like “quantity x product name”.
        """
        return f"{self.quantity} x {self.product.title}"

