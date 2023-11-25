from django.urls import path
from .views import toolView
urlpatterns = [
    path("",toolView,name="tool"),
]
