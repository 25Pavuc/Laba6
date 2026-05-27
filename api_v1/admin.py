from django.contrib import admin
from .models import Author, Book, Comment

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Администрирование авторов."""
    list_display = ['id', 'name', 'birth_date']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Администрирование книг."""
    list_display = ['id', 'title', 'author', 'published_date', 'created_at']
    list_filter = ['author', 'published_date']
    search_fields = ['title', 'description']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Администрирование комментариев."""
    list_display = ['id', 'book', 'text_preview', 'created_at']
    search_fields = ['text']

    def text_preview(self, obj):
        """Обрезает текст комментария до 50 символов для удобства отображения."""
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    text_preview.short_description = 'Комментарий'