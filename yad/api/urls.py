from django.urls import include, path

from . import views

app_name = "api"

urlpatterns = [
    path("nodes/<str:id>", views.NodesView.as_view(), name="node"),
    path("delete/<str:id>", views.DeleteView.as_view(), name="delete"),
    path("imports", views.ImportsView.as_view(), name="imports"),
    path("updates", views.UpdatesView.as_view(), name="updates"),
]
