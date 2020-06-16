from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from .apiviews import TaskDetailViewSet

router = DefaultRouter()
router.register(r'todo', TaskDetailViewSet)

app_name = 'ToDo'
urlpatterns = [
    path('', include(router.urls)),
]