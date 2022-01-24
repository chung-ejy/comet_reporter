from . import views
from django.urls import path

urlpatterns = [
    path("",views.errorView,name="error")
]