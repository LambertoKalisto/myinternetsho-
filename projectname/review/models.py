from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Reviews(models.Model):
    """
    Модель відгуку користувача.

    Attributes:
    - name (CharField): Ім'я користувача.
    - full_text (TextField): Текст відгуку.
    - rate (FloatField): Оцінка від 0 до 5.
    - date (DateTimeField): Дата створення відгуку.
    """
    name = models.CharField('Імя користувача', max_length=50)
    full_text = models.TextField('Відгук')
    rate = models.FloatField('Оцінка', validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ])
    date = models.DateTimeField('Дата')

    def __str__(self):
        """
        Повертає рядкове представлення об'єкту - ім'я користувача.

        Returns:
        - str: Рядок - ім'я користувача.
        """
        return self.name

    class Meta:
        """
        Клас метаданих моделі Reviews.

        Attributes:
        - verbose_name (str): Описова назва одного об'єкту моделі.
        - verbose_name_plural (str): Описова назва багатьох об'єктів моделі.
        """
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'