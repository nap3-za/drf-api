from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name="app-name"


app_name_router = DefaultRouter()
app_name_router.register("app-names", views.AbsentRecordsViewSet, basename="app-name")


urlpatterns [
	app_name_router.urls
] 

