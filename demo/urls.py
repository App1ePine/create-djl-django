from django.urls import path

from .views import demo_view

app_name = "demo"

urlpatterns = [path("python_model/demo_view/", demo_view, name="demo_view")]
