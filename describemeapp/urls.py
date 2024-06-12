from django.urls import path
from . import views

app_name = "describemeapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("esp", views.esp, name="esp"),
    path("eng", views.eng, name="eng")
]