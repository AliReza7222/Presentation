from django.urls import path

from presentations.api.v1.views import CreatePresentationView, CreateTagView

app_name = "presentations"

urlpatterns = [
    path("create/", CreatePresentationView.as_view(), name='create_presentation'),
    path("create/tag/", CreateTagView.as_view(), name="create_tag")
]
