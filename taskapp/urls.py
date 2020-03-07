
from django.urls import path
from taskapp import views


urlpatterns = [
    path('', views.consume_api, name="consumeapi"),


]
