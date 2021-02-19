from uuid import uuid1

from django_filters.rest_framework import DjangoFilterBackend
from api_yamdb import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Review
from titles.models import Category, Genre, Title
from users.models import User
from .filters import TitleFilter
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAdminOrStaff
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserEmailSerializer, UserLoginSerializer,
                          UserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    """"Модель обработки запросов к произведениям"""
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

    def category_genre_perform(self, serializer):
        category_slug = self.request.data['category']
        category = get_object_or_404(Category, slug=category_slug)
        genre_slug = self.request.POST.getlist('genre')
        genres = Genre.objects.filter(slug__in=genre_slug)
        serializer.save(
            category=category,
            genre=genres,
        )

    def perform_create(self, serializer):
        """"
        Создание нового произведения, возможно только администротором
        """
        self.category_genre_perform(serializer)

    def perform_update(self, serializer):
        """"
        Изменение характеристик существующего произведения,
        возможно только администротором
        """
        self.category_genre_perform(serializer)


class GenreCategoryMixinViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Миксин для классов жанров и категорий"""
    queryset = None
    serializer_class = None
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = "slug"
    permission_classes = [IsAdminOrReadOnly]


class CategoryViewSet(GenreCategoryMixinViewSet):
    """Модель обработки категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(GenreCategoryMixinViewSet):
    """Модель обработки жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Модель обработки отзывов"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrStaff, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def serializing_and_rating_calculation(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, title=title)
        title.rating = (Review.objects.filter(title=title).aggregate(Avg(
            'score'))['score__avg'])
        title.save(update_fields=['rating'])

    def perform_create(self, serializer):
        self.serializing_and_rating_calculation(serializer)

    def perform_update(self, serializer):
        self.serializing_and_rating_calculation(serializer)

    def get_serializer_context(self):
        return {'title_id': self.kwargs['title_id'], 'request': self.request}


class CommentViewSet(viewsets.ModelViewSet):
    """Модель обработки комментариев"""
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrStaff, IsAuthenticatedOrReadOnly]

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        return review

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)


class ConfirmationCodeView(APIView):

    def post(self, request):
        """Обработка POST запроса на получение Confirmation code"""
        serializer = UserEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        secret = str(uuid1())  # генерация уникального ключа
        User.objects.create(email=email, secret=secret)
        send_mail(
            'Ваш секретный код',
            secret,
            settings.ADMIN_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """ Модель авторизации пользователя """

    def post(self, request):
        """
        Обработка POST запроса на получение JWT по email и секретному коду
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']

        user = get_object_or_404(User, email=email)

        refresh = RefreshToken.for_user(user)  # получаем токен

        return Response(
            {"access": str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )


class UserViewSet(viewsets.ModelViewSet):
    """Модель обработки запросов пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdmin, IsAuthenticated)
    pagination_class = PageNumberPagination
    lookup_field = "username"

    @action(
        detail=False, methods=['PATCH', 'GET'],
        permission_classes=(
            IsAuthenticated,
        )
    )
    def me(self, request):
        serializer = UserSerializer(request.user,
                                    data=request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
