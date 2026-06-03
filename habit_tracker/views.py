from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny

from habit_tracker.models import Habit
from habit_tracker.pagination import MyPagination
from habit_tracker.serializers import HabitSerializer, PublicHabitSerializer


class OwnedHabitMixin:

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = getattr(self.request, "user", None)
        if not user or not user.is_authenticated:
            return Habit.objects.none()
        return Habit.objects.filter(owner=user)


class HabitCreateAPIView(CreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Habit.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HabitRetrieveAPIView(OwnedHabitMixin, RetrieveAPIView):
    serializer_class = HabitSerializer


class HabitUpdateAPIView(OwnedHabitMixin, UpdateAPIView):
    serializer_class = HabitSerializer


class HabitDestroyAPIView(OwnedHabitMixin, DestroyAPIView):
    serializer_class = HabitSerializer


class HabitListAPIView(OwnedHabitMixin, ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = MyPagination


class PublicHabitListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PublicHabitSerializer
    pagination_class = MyPagination
    queryset = Habit.objects.filter(is_public=True)
 
