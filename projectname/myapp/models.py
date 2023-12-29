from django.db import models

class Product(models.Model):
    title = models.CharField('Назва', max_length=50)
    description = models.CharField('Опис товару', max_length=250)
    price = models.FloatField('Ціна')
    image = models.ImageField('Картинка', upload_to='images/')
    date = models.DateTimeField('Дата публікації')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'

class Cart(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    def sum(self):
        return self.product.price * self.quantity
    def __str__(self):
        return self.product.title

class Order(models.Model):
    Name = models.CharField("Ім'я", max_length=50)
    SurName = models.CharField("Прізвише", max_length=50)
    Adress = models.CharField("Адресса відправки", max_length=250)
    PhoneNumber = models.IntegerField("Номер телефону")
    cart_items = models.ManyToManyField(Cart)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Закази'