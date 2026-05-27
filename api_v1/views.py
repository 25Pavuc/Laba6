from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response

from .models import Author, Book, Comment
from .serializers import AuthorSerializer, BookSerializer, CommentSerializer

# Объявляем класс, наследующий ModelViewSet — готовый набор действий для CRUD (list, retrieve, create, update, partial_update, destroy)
class AuthorViewSet(viewsets.ModelViewSet):
    # Документирующая строка: объясняет назначение класса, особенности кеширования и фильтрации
    """Представление для работы с авторами.

    Поддерживает все CRUD-операции, включая массовое создание,
    обновление и удаление. GET-запросы кешируются на 15 минут.
    Фильтрация списка возможна по GET-параметру `name` (поиск по подстроке).
    """

    # Указываем, что для преобразования объектов в JSON и обратно используется AuthorSerializer
    serializer_class = AuthorSerializer
    # Определяем базовый набор записей: все объекты модели Author
    queryset = Author.objects.all()

    # Переопределяем метод, чтобы добавить фильтрацию по имени
    def get_queryset(self):
        # Вызываем родительский метод, получая стандартный queryset
        qs = super().get_queryset()
        # Берём из параметров строки запроса значение по ключу 'name'
        name = self.request.query_params.get('name')
        # Если клиент передал имя, отбираем только тех авторов, чьё имя содержит эту подстроку (без учёта регистра)
        if name:
            qs = qs.filter(name__icontains=name)
        # Возвращаем отфильтрованный (или исходный) queryset
        return qs

    def list(self, request, *args, **kwargs):
        # Просто вызываем родительскую реализацию — она вернёт список авторов в JSON
        return super().list(request, *args, **kwargs)

    # кешируем детальный просмотр одного автора
    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        # Родительский retrieve извлекает объект по id и отдаёт его данные
        return super().retrieve(request, *args, **kwargs)

    # Обработчик POST-запросов — создание нового автора (или нескольких)
    def create(self, request, *args, **kwargs):
        # Проверяем, является ли тело запроса списком (массовое создание) или одиночным объектом
        many = isinstance(request.data, list)
        # Создаём сериализатор: если many=True, то он ожидает список объектов
        serializer = self.get_serializer(data=request.data, many=many)
        # Запускаем валидацию, при ошибке автоматически вернётся ответ 400 с деталями
        serializer.is_valid(raise_exception=True)
        # Сохраняем новые объекты в базе
        self.perform_create(serializer)
        # Собираем заголовки ответа, например Location для созданного ресурса
        headers = self.get_success_headers(serializer.data)
        # Отдаём сериализованные данные с HTTP-статусом 201 Created
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Полное обновление (PUT) одного или списка авторов
    def update(self, request, *args, **kwargs):
        # Снова определяем, массовая операция или нет
        many = isinstance(request.data, list)
        if many:
            # Для списка из каждого элемента извлекаем id и находим соответствующий объект в базе
            instances = [Author.objects.get(pk=item['id']) for item in request.data]
            # Создаём сериализатор с найденными объектами и новыми данными, many=True
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            # Для одиночного объекта получаем его стандартным методом (по id из URL)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        # Валидируем данные
        serializer.is_valid(raise_exception=True)
        # Сохраняем изменения
        self.perform_update(serializer)
        # Возвращаем обновлённые данные
        return Response(serializer.data)

    # Частичное обновление (PATCH) — работает как update, но с partial=True
    def partial_update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Author.objects.get(pk=item['id']) for item in request.data]
            # Обратите внимание: partial=True разрешает опускать обязательные поля
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # Удаление (DELETE) — одного или нескольких авторов
    def destroy(self, request, *args, **kwargs):
        # Проверяем, передан ли GET-параметр ids
        ids = request.query_params.get('ids')
        if ids:
            # Разбиваем строку с id (например, "1,2,3") на список целых чисел
            ids_list = [int(pk) for pk in ids.split(',')]
            # Удаляем всех авторов, чьи id попали в этот список
            Author.objects.filter(pk__in=ids_list).delete()
            # Возвращаем 204 No Content — стандартный ответ успешного удаления
            return Response(status=status.HTTP_204_NO_CONTENT)
        # Если ids нет, вызываем стандартный destroy, который удаляет одного автора по id из URL
        return super().destroy(request, *args, **kwargs)

class BookViewSet(viewsets.ModelViewSet):
    """Представление для работы с книгами.

    Поддерживает все CRUD-операции, включая массовые создание, обновление,
    удаление. GET-запросы кешируются. Можно фильтровать по автору и названию.
    """

    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get_queryset(self):
        """Фильтрация книг по `author_id` и `title`."""
        qs = super().get_queryset()
        author_id = self.request.query_params.get('author_id')
        title = self.request.query_params.get('title')
        if author_id:
            qs = qs.filter(author_id=author_id)
        if title:
            qs = qs.filter(title__icontains=title)
        return qs

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """POST-создание одной или нескольких книг."""
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """PUT-обновление одной книги или списка (каждый объект требует `id`)."""
        many = isinstance(request.data, list)
        if many:
            instances = [Book.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """PATCH-частичное обновление одной или нескольких книг."""
        many = isinstance(request.data, list)
        if many:
            instances = [Book.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """DELETE-удаление одной книги или списка через параметр `ids`."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Book.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)

class CommentViewSet(viewsets.ModelViewSet):
    """Представление для работы с комментариями.

    Поддерживает все CRUD-операции с массовыми действиями.
    GET-запросы кешируются, фильтрация по `book_id`.
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        """Фильтрация комментариев по книге."""
        qs = super().get_queryset()
        book_id = self.request.query_params.get('book_id')
        if book_id:
            qs = qs.filter(book_id=book_id)
        return qs

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """POST-создание одного или нескольких комментариев."""
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """PUT-обновление одного комментария или списка (каждый объект требует `id`)."""
        many = isinstance(request.data, list)
        if many:
            instances = [Comment.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """PATCH-частичное обновление одного или нескольких комментариев."""
        many = isinstance(request.data, list)
        if many:
            instances = [Comment.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """DELETE-удаление одного комментария или списка через параметр `ids`."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Comment.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)