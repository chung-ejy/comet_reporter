from . import views
from django.urls import path

urlpatterns = [
    path("",views.tradeView,name="trade")
]