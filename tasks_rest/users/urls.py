from django.urls import path

from .views import (
    UserListCreateApiView,
    UserRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('', UserListCreateApiView.as_view(), name='user_api'),
    path('<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user_api')
]