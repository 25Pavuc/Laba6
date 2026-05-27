from rest_framework import serializers
from .models import Author, Book, Comment

class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Author.
    Преобразует объекты авторов в JSON и обратно,
    включая поля id, name, birth_date и bio.
    """
    class Meta:
        model = Author
        fields = ['id', 'name', 'birth_date', 'bio']

class BookSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Book.
    При чтении отдаёт вложенный объект автора.
    При создании и обновлении принимает только id автора в поле author_id.
    """
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True
    )

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'published_date',
            'author', 'author_id', 'genres', 'created_at'
        ]

class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment.
    При создании требует указания id книги (book_id),
    при чтении отдаёт краткую информацию о книге.
    """
    book = serializers.StringRelatedField(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source='book', write_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'book', 'book_id', 'text', 'created_at']        