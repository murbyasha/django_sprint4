from django.db import models


class PublishedModel(models.Model):

    is_published = models.BooleanField('Опубликовано', default=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True
