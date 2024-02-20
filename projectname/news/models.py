from django.db import models

class Articles(models.Model):
    """
    The model presents statistics on the website.

    Attributes:
    - title (CharField): Title of the article.
    - anons (CharField): Announcement of statistics.
    - full_text (TextField): Full text of the article.
    - date (DateTimeField): Date of publication of the article.
    """
    title = models.CharField('Название', max_length=50)
    anons = models.CharField('Анонс', max_length=250)
    full_text = models.TextField('Статья')
    date = models.DateTimeField('Дата публикации')

    def __str__(self) -> str:
        """
        Turns around the presentation of the object - the name of the novelty.

        Returns:
        - str: Row - the name of the novelty.
        """
        return self.title

    class Meta:
        """
        Metaclass for configuration of the Articles model.

        Attributes:
        - verbose_name (str): Describes the name of one model object.
        - verbose_name_plural (str): Descriptive names of many objects in the model.
        """
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
