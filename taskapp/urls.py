
from django.urls import path
from taskapp import views


urlpatterns = [
    path('', views.shopify_api),


]
