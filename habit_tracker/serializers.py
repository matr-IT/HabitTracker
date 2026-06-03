from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from habit_tracker.models import Habit


class HabitSerializer(ModelSerializer):

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("owner",)

    def validate(self, data):
        if data.get("connected_habit") and data.get("reward"):
            raise serializers.ValidationError("Можно указать либо связь, либо награду.")
        return data

    def validate_time_to_complete(self, value):
        if not (1 <= value <= 120):
            raise serializers.ValidationError(
                "Время на выполнение должно быть от 1 до 120 секунд."
            )
        return value

    def validate_connected_habit(self, value):
        if value and not value.is_pleasant:
            raise serializers.ValidationError(
                "В связанные привычки можно добавить только привычки с признаком приятной привычки."
            )
        return value

    def validate_is_pleasant(self, value):
        if value and (
            self.initial_data.get("reward") or self.initial_data.get("connected_habit")
        ):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )
        return value

    def validate_periodicity(self, value):
        if value < 1 or value > 7:
            raise serializers.ValidationError(
                "Периодичность должна быть от 1 до 7 раз в неделю."
            )
        return value


class PublicHabitSerializer(ModelSerializer):

    class Meta:
        model = Habit
        fields = ("id", "action", "place")
