from django.urls import path
from . import views

urlpatterns = [
    path("", views.predict_plant, name="predict_plant"),
    path("my_preds/", views.get_my_preds, name="my_preds")
]
