from django.urls import path

from .views import (
    TaskListCreateApiView,
    TaskRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('', TaskListCreateApiView.as_view(), name='task_api'),
    path('<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task_api')
]