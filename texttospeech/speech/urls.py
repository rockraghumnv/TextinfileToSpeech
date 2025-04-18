from django.urls import path
from . import views

app_name="speech"

urlpatterns = [
    path("index/",views.index, name="index"),
    path("speech/",views.speech,name="speech"),
]