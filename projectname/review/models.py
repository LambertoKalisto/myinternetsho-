from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Reviews(models.Model):
    """
    User feedback model.

    Attributes:
    - name (CharField): Username.
    - full_text (TextField): Feedback text.
    - rate (FloatField): Rate from 0 to 5.
    - date (DateTimeField): The date the review was created.
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
        Returns a string representation of the username object.

        Returns:
        - str: String - username.
        """
        return self.name

    class Meta:
        """
        Metadata class of the Reviews model.

        Attributes:
        - verbose_name (str): Descriptive name of one model object.
        - verbose_name_plural (str): Descriptive name of many model objects.
        """
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'