from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import Q

from phonenumber_field.modelfields import PhoneNumberField

from app.field_choices import (
	Genders,
)


# Create your models here.


class AccountQuerySet(models.QuerySet):

	def search(self, query=None):
		if query == None:
			return self.none()
		
		# If a query is 'Name Surname' 
		# Convert to 'Name','Surname'
		queries = query.split(" ")
		for query in queries:
			lookups += Q(Q(name__icontains=query) | Q(surname__icontains=query) | Q(username__icontains=query) | Q(phone_number__icontains=query) | Q(email__icontains=query) & Q(is_active=True))
		return self.filter(lookups)

class Account(AbstractBaseUser, PermissionsMixin):

	class AccountManager(BaseUserManager):
		
		def get_queryset(self):
			return AccountQuerySet(self.model, using=self.db)

		def search(self, query=None):
			return self.get_queryset().search(query=query)

		def create_user(self,name,surname,username,gender,phone_number=None,email=None,password=None):
			user = self.model(
				name=name,
				surname=surname,
				username=username,
				gender=gender,

				email=email,
				phone_number=phone_number,
				password=password,
			)
			user.set_password(password)
			user.save(using=self._db)
			
			return user

		def create_superuser(self,name,surname,username,gender,phone_number=None,email=None,password=None):
			user = self.create_user(
				name=name,
				surname=surname,
				username=username,
				gender=gender,

				email=email,
				phone_number=phone_number,
				password=password,
			)
			user.is_superuser = True
			user.save(using=self._db)
			return user

		def all_active(self):
			return self.all().filter(is_active=True)


	name 					= models.CharField(verbose_name="name", max_length=125, unique=False, null=False, blank=False)
	surname 				= models.CharField(verbose_name="surname", max_length=125, unique=False, null=False, blank=False)
	username				= models.CharField(verbose_name="username", max_length=125, unique=True, null=False, blank=False)
	gender 					= models.CharField(choices=Genders.choices, max_length=10, unique=False, null=False, blank=False)	
	
	email 					= models.EmailField(max_length=125, unique=True, null=True, blank=True)
	phone_number 			= PhoneNumberField(verbose_name="phone number", null=True, unique=True, blank=True, error_messages={"unique":"Phonenumber is already in use"})

	# char_field 				= models.CharField(max_length=255, unique=False, null=True, blank=True)
	# integer_field			= models.PositiveIntegerField(unique=True, null=True, blank=True)
	# date_field				= models.DateField(null=True, blank=True)

	# If false then the account is deleted
	is_active 				= models.BooleanField(default=True)

	date_joined				= models.DateTimeField(auto_now_add=True)
	last_login				= models.DateTimeField(auto_now=True)	
	
	is_admin				= models.BooleanField(default=False)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)


	USERNAME_FIELD = "username"
	REQUIRED_FIELDS = ["name", "surname", "gender", "email"]

	objects = AccountManager()

	def __str__(self):
		return self.full_names

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=["email", "phone_number", "username"],
				name="unique_undeleted_fields",
				condition=Q(is_active=True),
			)
		]

	@property 
	def full_names(self):
		return f"{self.name} {self.surname}"

	def update(self, **kwargs):
		Account.objects.filter(id=self.id).update(**kwargs)
		return Account.objects.get(id=self.id)

	# Set the account as innactive
	def deactivate(self):
		self.update(is_active=False)