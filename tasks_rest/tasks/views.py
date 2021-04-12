from django.db.models import Q
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from  .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated

class TaskListCreateApiView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        queryset = Task.objects.filter(user=self.request.user)
        search_term = self.request.query_params.get('search')
        if search_term:
            queryset = queryset.filter(Q(title__icontains=search_term) | Q(description__icontains=search_term))
        return queryset

class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
