from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count
from django.utils import timezone

User = get_user_model()


class BaseModel(models.Model):
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано', help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        abstract = True


class PostManager(models.QuerySet):

    def filter_posts(self):
        return self.filter(pub_date__lte=timezone.now(), is_published=True, category__is_published=True)

    def count_comments(self):
        return self.select_related('category', 'location', 'author').annotate(
            comments_count=Count('comments')
        ).order_by('-pub_date')

    def posts_comments(self):
        return self.filter_posts().count_comments()


class Category(BaseModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор', help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:20]


class Location(BaseModel):
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __Str__(self):
        return self.name[:20]


class Post(BaseModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(verbose_name='Дата и время публикации', help_text='Если установить дату и время в будущем — можно делать отложенные публикации.')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор публикации',related_name='posts')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория', related_name='posts')
    image = models.ImageField(upload_to='post_images', blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    objects = PostManager.as_manager()

    def __str__(self):
        return self.title[:20]


class Comment(BaseModel):
    text = models.TextField(verbose_name='Текст комментария')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Публикация')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

        def __str__(self):
            return self.text[:20]
