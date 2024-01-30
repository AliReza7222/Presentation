from django.urls import path

from presentations.api.v1.views import *

app_name = "presentations"

urlpatterns = [
    path("create/", CreatePresentationView.as_view(), name='create_presentation'),
    path("create/tag/", CreateTagView.as_view(), name="create_tag"),
    path("update/<int:pk>/", UpdatePresentationView.as_view(), name='update_presentation')
]
