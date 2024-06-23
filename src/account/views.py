from django.shortcuts import reverse
from django.contrib.auth import login, authenticate, logout
from rest_framework import (
	generics,
	status,
	pagination,
	mixins,
	viewsets,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from app import (
	permissions as app_permissions,
	custom_view_mixins,
)

from .serializers import (
	SignUpSerializer,
	SignInSerializer,
	AccountSerializer,
	AccountDeletionSerializer,
)

from account.models import Account


# Create your views here.


class SignUpView(generics.CreateAPIView):
	
	serializer_class = SignUpSerializer
	permission_classes = (app_permissions.IsNotAuthenticated,)

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)

		auth_user_account = authenticate(
			username=request.data.get("username"),
			password=request.data.get("password"))
		login(request, auth_user_account)
		headers = self.get_success_headers(serializer.data)

		response_data = {
			"user": AccountSerializer(auth_user_account, context=self.get_serializer_context()).data,
			"token": AuthToken.objects.create(auth_user_account)[1]
		}
		return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

	def perform_create(self, serializer):
		return serializer.save()


class SignInView(generics.GenericAPIView):
	serializer_class = SignInSerializer
	permission_classes = (app_permissions.IsNotAuthenticated,)

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		auth_user_account = serializer.validated_data
		login(request, auth_user_account)

		try:
			token = AuthToken.objects.get(auth_user_account)
		except Exception:
			token = AuthToken.objects.create(auth_user_account)

		response_data = {
			"user": AccountSerializer(auth_user_account, context=self.get_serializer_context()).data,
			"token": token[1]
		}
		return Response(response_data, status=status.HTTP_200_OK)


class AccountViewSetPagination(pagination.PageNumberPagination):
	page_size = 10
	page_size_query_param = "size"
	max_page_size = 25

# Listing & Retrieving & Updating(via settings)
class AccountViewSet(custom_view_mixins.CustomUpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet):

	queryset = Account.objects.all().order_by('-username')
	serializer_class = AccountSerializer
	pagination_class = AccountViewSetPagination


	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()

		# Used by react to send some get requests of more info 
		# if the authenticated user is viewing his own account
		is_auth_user = False
		if instance == request.user:
			is_auth_user = True 

		account_serializer = self.get_serializer(instance)

		# Add verbose information
		response_data = {
			"account":account_serializer.data,
			"isAuthUser": is_auth_user,
		}
		return Response(response_data)

	def perform_update(self, serializer):
		instance = self.get_object()
		if instance != self.request.user:
			return Response({"error":"You cannot update an account that doesn't belong to you"}, status=status.HTTP_403_FORBIDDEN)
		return serializer.save()

class AccountDeletionView(APIView):
	
	def post(self, request, *args, **kwargs):
		auth_user_account = request.user
		serializer = AccountDeletionSerializer(data=request.data, instance=request.user)
		serializer.is_valid(raise_exception=True)
		auth_user_account.deactivate()
		return Response(status=status.HTTP_204_NO_CONTENT)

# Sends account data using authenticated user's api token
class RetrieveAccount(generics.RetrieveAPIView):
	
	serializer_class = AccountSerializer

	def get_object(self):
		return self.request.user

