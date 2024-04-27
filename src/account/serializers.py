import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import reverse
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import login, authenticate
from phonenumber_field.serializerfields import PhoneNumberField

from .models import Account

from app.validators import (
	choice_validator,
	date_validator,
	length_validator,
	email_validator,
	size_validator,
) 

from app.field_choices import (
	Genders,
)


class BaseAccountSerializer(serializers.ModelSerializer):

	class Meta:
		model = Account
		fields = [
			"name",
			"surname",
			"username",
			"gender",
			"email",
			"phone_number",
		]


	def validate_name(self, name):
		return length_validator(name, 1, for_serializer=True)

	def validate_surname(self, surname):
		return length_validator(surname, 1, for_serializer=True)

	def validate_username(self, username):
		return length_validator(username, 1, for_serializer=True)

	def validate_gender(self, gender):
		return choice_validator(gender, Genders.choices, for_serializer=True)

	def validate_email(self, email):
		return email_validator(email, for_serializer=True)

	# These have to be explicitly defined to work
	def create(self, validated_data):
		return None 
	def update(self, instance, validated_data):
		return None

class AccountListSerializer(serializers.ListSerializer):

	def to_representation(self, instance): 
		representation = super().to_representation(instance)
		# for account in representation:
		# 	try:
		# 		account_model = Account.objects.get(id=account["id"])
		# 		account["url"] = account_model.get_profile_url()
		# 	except Exception:
		# 		# This should never happen
		# 		pass
		# 	del account["dob"]
		# 	del account["gender"]
		# 	del account["physical_address"]
		# 	del account["phone_number"]
		# 	del account["email"]
		# 	del account["profile"]
		return representation

class AccountSerializer(BaseAccountSerializer):

	class Meta:
		list_serializer_class = AccountListSerializer
		model = Account
		fields = (
			"id",
			"name",
			"surname",
			"username",
			"gender",
			"email",
			"phone_number",
		)
		read_only_fields = (
			"id",
		)

	def validate_email(self, email):
		return email_validator(email, current_email=self.instance.email, for_serializer=True)

	def update(self, instance, validated_data):
		try:
			instance.update(
				email=validated_data.get('email'),
				name=validated_data.get('name'),
				surname=validated_data.get('surname'),
				username=validated_data.get('username'),
				gender=validated_data.get('gender'),
				phone_number=validated_data.get('phone_number'),
			)
			
		except Exception as e:
			raise serializers.ValidationError({"error":str(e)})

		return instance

	# Nullyfying the create method
	def create(self, validated_data):
		pass


class SignUpSerializer(BaseAccountSerializer):

	password2   					= serializers.CharField(style={"input_type":"password"}, write_only=True)

	class Meta:
		model = Account
		fields = [
			"name",
			"surname",
			"username",
			"gender",
			"email",
			"password",
			"password2"
		]
		extra_kwargs = {
			"password":{"write_only":True},
			"password2":{"write_only":True},
		}


	def create(self, validated_data):
		password = validated_data.get('password').replace(" ","")
		password2 = validated_data.get("password2").replace(" ","")
		if password != password2:
			raise serializers.ValidationError({"password": "Passwords do not match"})

		account = Account.objects.create_user(
			name=validated_data.get('name'),
			surname=validated_data.get('surname'),
			username=validated_data.get('username'),
			email=validated_data.get('email'),
			gender=validated_data.get('gender'),
			phone_number=validated_data.get('phone_number'),
			password=password,
		)

		return account

	def save(self):
		if not self.instance is None:
			self.update(instance=self.instance, validated_data=self.validated_data)
		else:
			self.create(validated_data=self.validated_data)

		return self.instance

class SignInSerializer(serializers.Serializer):

	# Authentication field here	
	password	   				 	= serializers.CharField(style={"input_type":"password"}, write_only=True)


	def validate(self, data):
		try:
			phone_number = data.get("phone_number")
			password = data.get("password")
			account = authenticate(phone_number=phone_number, password=password)
			
			if not account.is_active:
				raise ValueError("The account has been deleted");

		except Exception:
			raise serializers.ValidationError({"error":"Invalid credentials"})

		return account


class AccountDeletionSerializer(serializers.Serializer):

	# Authentication field here
	password   	 				 	= serializers.CharField(style={"input_type":"password"}, write_only=True)


	def validate(self, attrs):
		auth_field = attrs.get("auth_field", None)
		password = attrs.get("password", None)
		if not auth_field or not password:
			raise serializers.ValidationError({"error":"No field may be empty."})

		user = authenticate(auth_field=auth_field, password=password)
		if user == None:
			raise serializers.ValidationError({"error":"Invalid credentials"})
		elif self.instance != user:
			raise serializers.ValidationError({"error":"You are not allowed to delete another person's account"})

		return attrs
