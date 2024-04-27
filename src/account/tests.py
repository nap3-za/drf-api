import datetime

from random import randint

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import Group
from django.db import transaction

from rest_framework import status
from rest_framework.test import APITestCase 

from .models import Account

from app.field_choices import AccountTypes,SignUpTokenStatuses 


class AccountTests(APITestCase):

	@classmethod
	def setUpTestData(cls):

		# Create an admin account
		account = Account.objects.create_user(
			# auth_field
			name=f"admin",
			surname=f"admin",
			username=f"admin",
			gender="MLE",
			password="root.1352",
		)

	def test_account_sign_up(self):
		user_data = {
			"phone_number":f"+27123456785",
			"name":f"user_name",
			"surname":f"user_surname",
			"username":f"username",
			"gender":"MLE",
			"password":"root.1352",
			"password2":"root.1352",
		}

		sign_up_url = reverse("sign-up")
		response = self.client.post(sign_up_url, user_data, format="json")

		sign_out_url = reverse("knox_logout")
		self.client.get(sign_out_url)

		# Necessary Checks
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(str(account.phone_number), f"+27123456785")
		self.assertEqual(str(account), f"{account.name} {account.surname}")


	def test_account_sign_in_out(self):
		data = {
			"phone_number":"+27123456780",
			"password":"root.1352"
		}

		# Signing in
		sign_in_url = reverse("sign-in")
		sign_in_response = self.client.post(sign_in_url, data, format="json")
		self.assertEqual(sign_in_response.status_code, status.HTTP_200_OK)
		self.assertTrue(sign_in_response.data.get("token"))

		# Adding Authorization Token
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {sign_in_response.data['token']}")

		# Signing out
		sign_out_url = reverse("knox_logout")
		sign_out_response = self.client.post(path=sign_out_url)

	def test_account_update_delete(self):

		# Signing In
		sign_in_data = {
			"phone_number":"+27123456780",
			"password":"root.1352"
		}
		
		sign_in_url = reverse("sign-in")
		sign_in_response = self.client.post(sign_in_url, sign_in_data, format="json")

		# Adding Authorization Token
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {sign_in_response.data['token']}")
		
		# Testing Update
		update_data = {
			"email":f"adminupdated@test.com",
			"gender":"FML",
			"phone_number":f"+27726060470",
			"name":"user_name_updated",
			"surname":"user_surname_updated",
			"username": "username_updated"
		}
		account = Account.objects.get(phone_number="+27123456780")

		update_url = f"{reverse('account:account-list')}{str(account.pk)}/"
		update_response = self.client.put(update_url, update_data, format="json")
		
		account = Account.objects.get(phone_number="+27726060470")
		self.assertEqual(account.email, update_data["email"])
		self.assertEqual(account.name, update_data["name"])
		self.assertEqual(account.surname, update_data["surname"])
		self.assertEqual(account.username, update_data["username"])
		self.assertEqual(account.gender, update_data["gender"])
		self.assertEqual(account.phone_number, update_data["phone_number"])


		# Testing Delete
		deactivation_url = reverse("account:account-delete")
		deactivation_data = {
			"phone_number":"+27726060470",
			"password":"root.1352",
		}

		deactivation_response = self.client.post(deactivation_url, deactivation_data, format="json")
		self.assertEqual(deactivation_response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(Account.objects.get(email="adminupdated@test.com").is_active, False)

	def test_account_extras(self):
		pass




