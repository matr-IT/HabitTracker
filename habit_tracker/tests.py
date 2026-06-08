from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from habit_tracker.models import Habit


class HabitCRUDTest(TestCase):
	def _create_user(self, **kwargs):
		User = get_user_model()
		data = dict(email="user@example.com", chat_id="chat123")
		data.update(kwargs)
		user = User.objects.create(**data)
		user.set_password(data.get("password", "pass"))
		user.save()
		return user

	def setUp(self):
		self.client = APIClient()
		self.user = self._create_user(email="owner@example.com")
		self.other = self._create_user(email="other@example.com")

	def test_create_habit(self):
		self.client.force_authenticate(self.user)
		url = reverse("habit_tracker:create")
		payload = {
			"place": "Home",
			"time": "08:00:00",
			"action": "Meditate",
			"is_pleasant": False,
			"periodicity": 3,
			"reward": "",
			"time_to_complete": 60,
			"is_public": False,
		}
		resp = self.client.post(url, payload, format="json")
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		self.assertTrue(Habit.objects.filter(owner=self.user, action="Meditate").exists())

	def test_retrieve_habit(self):
		habit = Habit.objects.create(
			owner=self.user,
			place="Gym",
			time="07:00:00",
			action="Workout",
			is_pleasant=False,
			periodicity=4,
			time_to_complete=30,
			is_public=False,
		)
		self.client.force_authenticate(self.user)
		url = reverse("habit_tracker:detail", kwargs={"pk": habit.pk})
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertEqual(resp.data.get("action"), "Workout")

	def test_update_habit_by_owner_and_forbidden_for_others(self):
		habit = Habit.objects.create(
			owner=self.user,
			place="Office",
			time="09:00:00",
			action="Read",
			is_pleasant=False,
			periodicity=2,
			time_to_complete=20,
			is_public=False,
		)
		update_url = reverse("habit_tracker:update", kwargs={"pk": habit.pk})

		self.client.force_authenticate(self.other)
		resp = self.client.patch(update_url, {"action": "Write"}, format="json")
		self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

		self.client.force_authenticate(self.user)
		resp = self.client.patch(update_url, {"action": "Write"}, format="json")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		habit.refresh_from_db()
		self.assertEqual(habit.action, "Write")

	def test_delete_habit(self):
		habit = Habit.objects.create(
			owner=self.user,
			place="Park",
			time="06:00:00",
			action="Run",
			is_pleasant=False,
			periodicity=5,
			time_to_complete=40,
			is_public=False,
		)
		delete_url = reverse("habit_tracker:delete", kwargs={"pk": habit.pk})
		self.client.force_authenticate(self.other)
		resp = self.client.delete(delete_url)
		self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

		self.client.force_authenticate(self.user)
		resp = self.client.delete(delete_url)
		self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Habit.objects.filter(pk=habit.pk).exists())

	def test_list_owned_habits(self):
		Habit.objects.create(
			owner=self.user,
			place="Home",
			time="08:00:00",
			action="A",
			is_pleasant=False,
			periodicity=1,
			time_to_complete=10,
			is_public=False,
		)
		Habit.objects.create(
			owner=self.other,
			place="Home",
			time="08:00:00",
			action="B",
			is_pleasant=False,
			periodicity=1,
			time_to_complete=10,
			is_public=False,
		)
		self.client.force_authenticate(self.user)
		url = reverse("habit_tracker:list")
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		actions = [i.get("action") for i in resp.data.get("results", resp.data)]
		self.assertIn("A", actions)
		self.assertNotIn("B", actions)

	def test_public_list_accessible_to_anyone(self):
		Habit.objects.create(
			owner=self.user,
			place="Beach",
			time="10:00:00",
			action="Swim",
			is_pleasant=False,
			periodicity=1,
			time_to_complete=15,
			is_public=True,
		)
		Habit.objects.create(
			owner=self.user,
			place="Home",
			time="11:00:00",
			action="Cook",
			is_pleasant=False,
			periodicity=1,
			time_to_complete=15,
			is_public=False,
		)
		url = reverse("habit_tracker:public-list")
		client = APIClient()
		resp = client.get(url)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		actions = [i.get("action") for i in resp.data.get("results", resp.data)]
		self.assertIn("Swim", actions)
		self.assertNotIn("Cook", actions)

	def test_validation_conflicting_reward_and_connected_habit(self):
		pleasant = Habit.objects.create(
			owner=self.user,
			place="Park",
			time="07:00:00",
			action="Smile",
			is_pleasant=True,
			periodicity=1,
			time_to_complete=10,
			is_public=False,
		)
		self.client.force_authenticate(self.user)
		url = reverse("habit_tracker:create")
		payload = {
			"place": "Home",
			"time": "12:00:00",
			"action": "Test",
			"is_pleasant": False,
			"periodicity": 3,
			"reward": "Candy",
			"connected_habit": pleasant.pk,
			"time_to_complete": 30,
			"is_public": False,
		}
		resp = self.client.post(url, payload, format="json")
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

	def test_validation_time_to_complete_range(self):
		self.client.force_authenticate(self.user)
		url = reverse("habit_tracker:create")
		payload = {
			"place": "Home",
			"time": "12:00:00",
			"action": "Test2",
			"is_pleasant": False,
			"periodicity": 3,
			"reward": "",
			"time_to_complete": 200,
			"is_public": False,
		}
		resp = self.client.post(url, payload, format="json")
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
