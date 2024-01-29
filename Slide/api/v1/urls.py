from django.urls import path

from Slide.api.v1.views import CreateSlideView


app_name = "Slide"
urlpatterns = [
    path("create/", CreateSlideView.as_view(), name="create_slide")
]
