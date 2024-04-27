from django.db import models

# Create your models here.

class DataModelQuerySet(models.QuerySet):
	
	def search(self, query=None):
		if query == None:
			return self.none()
		lookups += Q(Q(DataModel_id__icontains=query) & Q(is_active=True))
		return self.filter(lookups)

# Input : DataModel_id
class DataModel(models.Model):
	
	class DataModelManager(models.Manager):

		def create(self, DataModel_id):
			DataModel = self.model(
				DataModel_id=DataModel_id
			)
			DataModel.save(using=self._db)
			return DataModel

		def get_queryset(self):
			return DataModelQuerySet(self.model, using=self._db)

		def search(self, query=None):
			return self.get_queryset().search(query=query)

		def all_active(self):
			return self.all().filter(is_active=True)

	# char_field 				= models.CharField(max_length=255, unique=False, null=True, blank=True)
	# integer_field				= models.PositiveIntegerField(unique=True, null=True, blank=True)
	# date_field				= models.DateField(null=True, blank=True)

	DataModel_OTO				= models.OneToOneField(
		"app.AppModel",
		related_name="DataModel",
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
	)
	DataModel_FK				= models.ForeignKey(
		"AppModel",
		related_name="DataModels",
		related_query_name="DataModel",
		on_delete=models.PROTECT,
		null=True,
		blank=False,
	)

	is_active    				= models.BooleanField(default=True)
	
	objects = DataModelManager()

	def __str__(self):
		return self.DataModel_id

	def update(self, **kwargs):
		DataModel.objects.filter(id=self.id).update(**kwargs)

	def deactivate(self):
		self.update(is_active=False)
