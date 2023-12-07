from django.urls import path
from .views import PostListCreateView, PostDetailView, post_list, post_detail
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_schema_view(
openapi.Info(
        title="ToDoApp",
        default_version='v1',
        description="Aplicación Web para tareas",
        terms_of_service="",
        contact=openapi.Contact(email="rosaljose125@gmail.com"),
        license=openapi.License(name="Copyright all rights reserved")
    ),
    public=True,
    permission_classes = (permissions.AllowAny,),
)


urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/', post_list, name='post-list'),
    path('posts/<int:pk>/', post_detail, name='post-detail-template'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui')
]