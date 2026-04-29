from django.contrib import admin

from .models import Category, Comment, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'text_short',
        'location',
        'category',
        'pub_date',
        'is_published',
    )
    list_editable = (
        'location',
        'category',
        'pub_date',
        'is_published',
    )
    search_fields = (
        'title',
        'text',
        'location',
    )
    list_page = 10

    @staticmethod
    @admin.display(description='Текст')
    def text_short(object: Post) -> str:
        return f'{object.text[:50]}...'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'description_short',
        'slug',
        'is_published',
        'created_at',
    )
    list_editable = (
        'slug',
    )
    list_filter = (
        'title',
        'description',
    )
    list_page = 10

    @staticmethod
    @admin.display(description='Описание')
    def description_short(object: Category) -> str:
        return f'{object.description[:50]}...'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    list_filter = ('name',)
    list_page = 10

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        'text',
        'post',
        'author',
        'created_at',
    )
    list_filter = ('text',)
    list_page = 10
