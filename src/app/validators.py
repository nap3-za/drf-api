from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from .utils import field_choices_to_list


validation_error_type = {
	True:serializers.ValidationError,
	False:ValueError,
}

def choice_validator(selected, choices, for_serializer=False):
	error = validation_error_type[for_serializer]

	if selected == None or ((type(selected) == str) and (selected.replace(" ","") == "")):
		raise error("This field may not be blank.")

	# First condition is for cases where 
	# choices is not a nested set
	if (not selected in choices) and (not selected in field_choices_to_list(choices)):
		raise error(f"{selected} is not a valid choice.")
	
	return selected

def date_validator(date, for_serializer=False):
	error = validation_error_type[for_serializer]

	if not date:
		raise error("This field may not be blank.")

	if date > timezone.now().date():
		raise error(f"{date} is not a valid date")
	
	return date

def size_validator(integer, min_size=None, max_size=None, for_serializer=False):
	error = validation_error_type[for_serializer]

	if not integer or type(integer) != int:
		raise error("This field may not be blank.")

	if min_size and integer < min_size:
		raise error(f"{integer} is too small")

	if max_size and integer > max_size:
		raise error(f"{integer} is too big")
	
	return integer

def length_validator(text, min_len, for_serializer=False):
	error = validation_error_type[for_serializer]

	if not text or type(text) != str:
		raise error("This field may not be blank.")

	if len(text) <= min_len:
		raise error(f"{text} is too small")
	
	return text 

def email_validator(email, current_email=None, for_serializer=False, **kwargs):
	
	obj = None
	if kwargs.get("obj"):
		obj = kwargs.get("obj")
	else:
		from account.models import Account
		obj = Account

	error = validation_error_type[for_serializer]

	# If a new account is being created
	if current_email == None:
		if obj.objects.all_active().filter(email=email).count() >= 1:
			raise error(f"{email} is already registered")
	else:
		# If there is an account with the email and
		# the new email is not the same as the current email
		if (obj.objects.all_active().filter(email=email).count() >= 1) and (email != current_email):
			raise error(f"{email} is already registered")

	return email

def presence_validator(data, data_name, for_serializer=False):
	error = validation_error_type[for_serializer]

	if (data == None) or (type(data) == str and data.replace(" ","") == ""):
		raise error(f"{data_name} cannot be blank.")

	return data
