from django.urls import path

from habit_tracker.apps import HabitTrackerConfig
from habit_tracker.views import (
    HabitCreateAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
    HabitDestroyAPIView,
    HabitListAPIView,
    PublicHabitListAPIView,
)

app_name = HabitTrackerConfig.name

urlpatterns = [
    path("create/", HabitCreateAPIView.as_view(), name="create"),
    path("<int:pk>/detail/", HabitRetrieveAPIView.as_view(), name="detail"),
    path("<int:pk>/update/", HabitUpdateAPIView.as_view(), name="update"),
    path("<int:pk>/delete/", HabitDestroyAPIView.as_view(), name="delete"),
    path("list/", HabitListAPIView.as_view(), name="list"),
    path("public-list/", PublicHabitListAPIView.as_view(), name="public-list"),
]
