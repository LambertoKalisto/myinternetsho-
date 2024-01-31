from django.db import models

class Articles(models.Model):
    """
    Модель представляє статті на сайті.

    Attributes:
    - title (CharField): Назва статті.
    - anons (CharField): Анонс статті.
    - full_text (TextField): Повний текст статті.
    - date (DateTimeField): Дата публікації статті.
    """
    title = models.CharField('Название', max_length=50)
    anons = models.CharField('Анонс', max_length=250)
    full_text = models.TextField('Статья')
    date = models.DateTimeField('Дата публикации')

    def __str__(self) -> str:
        """
        Повертає рядкове представлення об'єкту - назва новини.

        Returns:
        - str: Рядок - назва новини.
        """
        return self.title

    class Meta:
        """
        Метаклас для конфігурації моделі Articles.

        Attributes:
        - verbose_name (str): Описова назва одного об'єкту моделі.
        - verbose_name_plural (str): Описова назва багатьох об'єктів моделі.
        """
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
