from django.urls import path

from .views import *

app_name = "presentation"

urlpatterns = [
    path("create/", CreatePresentationView.as_view(), name='create_presentation'),
    path("update/<int:pk>/", UpdatePresentationView.as_view(), name='update_presentation'),
    path("delete/<int:pk>/", DeletePresentationView.as_view(), name='delete_presentation'),
    path("list/", ListPresentationView.as_view(), name='list_presentation'),
    path("<int:pk>/", PresentationView.as_view(), name="presentation_view"),
    path("<str:slug>/", PresentationBySlugView.as_view(), name="presentation_by_slug"),
]
