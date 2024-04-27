import datetime

from django.shortcuts import reverse
from rest_framework import serializers

from app.validators import (
	choice_validator,
	date_validator,
	length_validator,
	size_validator,
) 

from .models import DataModel



class DataModelListSerializer(serializers.ListSerializer):

	def to_representation(self, instance): 
		representation = super().to_representation(instance)
		return representation

class DataModelSerializer(serializers.ModelSerializer):

	class Meta:
		list_serializer_class = DataModelListSerializer
		model = DataModel
		fields = (
			"id",
			# ...
		)

		read_only_fields = (
			"id",
		)

	def to_representation(self, instance):
		representation = super().to_representation(instance)	
		return representation

	def validate_field(self, reason):
		return length_validator(reason, 1, for_serializer=True)

	def update(self, instance, validated_data):
		instance.update(
			field=validated_data.get("field"),
		)

		return instance

	def save(self):
		if not self.instance is None:
			self.update(instance=self.instance, validated_data=self.validated_data)
		else:
			try:
				self.instance = DataModel.objects.create(
					field=self.validated_data.get("field"),
				)
			except Exception as e:
				raise serializers.ValidationError({"error":"An error occured, Please try again"})

		return self.instance
