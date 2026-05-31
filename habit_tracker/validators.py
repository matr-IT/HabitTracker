from rest_framework.serializers import ValidationError

def validate_connection_or_reward(habit):
    if habit.connection and habit.reward:
        raise ValidationError("Можно указать либо связь, либо награду.")