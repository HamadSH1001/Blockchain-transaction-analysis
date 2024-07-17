from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="main"),
    path("view-graph", views.view_graph, name="view-graph"),
]
