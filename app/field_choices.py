from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


#== Accounts ==#

class Genders(TextChoices):
	MALE = "MLE", _("Male")
	FEMALE = "FML", _("Female")
	NON_BINARY = "NBN", _("Non-binary")