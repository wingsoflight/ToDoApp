from rest_framework import generics, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ToDo.models import Task
from .serializers import TaskSerializer

class TaskDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    @action(methods=['post'], detail=True)
    def execute(self, request, *args, **kwargs):
        task = self.get_object()
        task.completed = True
        task.save()
        return Response(TaskSerializer(task).data)