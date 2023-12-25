from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Reviews(models.Model):
    name = models.CharField('Імя користувача', max_length=50)
    full_text = models.TextField('Відгук')
    rate = models.FloatField('Оцінка', validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ])
    date = models.DateTimeField('Дата')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'