from django.db import models
from django.db.models import CASCADE


class Habit(models.Model):
    owner = models.ForeignKey(
        "users.User",
        on_delete=CASCADE,
        verbose_name="Владелец",
        help_text="Владелец привычки",
    )
    place = models.CharField(
        max_length=100,
        verbose_name="Место",
        help_text="Где вы хотите развить привычку?",
    )
    time = models.TimeField(
        verbose_name="Время",
        help_text="Когда вы хотите развить привычку?",
    )
    action = models.CharField(
        max_length=100,
        verbose_name="Действие",
        help_text="Какое действие вы хотите развить в привычку?",
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Отметьте, если эта привычка приятная для вас",
    )
    connected_habit = models.ForeignKey(
        "self",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        help_text="Выберите привычку, с которой связана эта привычка",
    )
    periodicity = models.IntegerField(
        verbose_name="Периодичность",
        help_text="Сколько раз в неделю вы хотите развивать эту привычку?",
    )
    reward = models.CharField(
        max_length=100,
        verbose_name="Награда",
        help_text="Какую награду вы хотите получить за развитие этой привычки?",
        null=True,
        blank=True,
    )
    time_to_complete = models.IntegerField(
        verbose_name="Время на выполнение",
        help_text="Сколько секунд Вам требуется на выполнение привычки? (от 1 до 120)",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичная привычка",
        help_text="Отметьте, если вы хотите, чтобы эта привычка была видна другим пользователям",
    )

    class Meta:
        ordering = ["id"]

