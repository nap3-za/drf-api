
from django.shortcuts import reverse
from django.contrib.auth import login, authenticate, logout
from rest_framework import (
	status,
	pagination,
	viewsets,
)
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import (
	DataModelSerializer,
	DataModelListSerializer,
)
from .models import DataModel

# from app import permissions as app_permissions

class DataModelViewSetPagination(pagination.PageNumberPagination):
	page_size = 25
	page_size_query_param = "size"
	max_page_size = 75

class AbsentRecordsViewSet(viewsets.CustomModelViewSet):

	queryset = DataModel.objects.all()
	serializer_class = DataModelSerializer
	pagination_class = DataModelsViewSetPagination

	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		return Response(serializer.data)

	def list(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	def perform_create(self, serializer):
		return serializer.save()

	def perform_update(self, serializer):
		return serializer.save()

	def perform_destroy(self, instance):
		instance.delete()
		return None
