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
