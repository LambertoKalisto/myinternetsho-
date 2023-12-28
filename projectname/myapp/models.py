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

class Order(models.Model):
    Name = models.CharField("Ім'я", max_length=50)
    SurName = models.CharField("Прізвише", max_length=50)
    Adress = models.CharField("Адресса відправки", max_length=250)
    PhoneNumber = models.IntegerField("Номер телефону", max_length=10)