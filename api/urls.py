from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, ConfirmationCodeView,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UserLoginView,
                    UserViewSet)

v1_patterns = (
    [
        path('email', ConfirmationCodeView.as_view()),
        path('token', UserLoginView.as_view()),
    ]
)

v1_router = DefaultRouter()
v1_router.register(r'titles', TitleViewSet, basename='TitlesView')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='ReviewsView')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='ReviewsView'
)
v1_router.register(
    r'titles/(P<titles_id>\.+)/(?P<review_id>.+)/comments',
    CommentViewSet,
    basename='CommentsView'
)
v1_router.register(r'users', UserViewSet)
v1_router.register(r'categories', CategoryViewSet)
v1_router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('v1/auth/', include(v1_patterns)),
    path('v1/', include(v1_router.urls)),
]
