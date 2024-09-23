from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:Title>", views.Entry, name="Entry"),
    path("random", views.Random, name="Random"),
    path("NewPage", views.NewPage, name="NewPage"),
    path("EditPage/<str:Title>", views.EditPage, name="EditPage")
]
