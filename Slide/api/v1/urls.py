from django.urls import path

from Slide.api.v1.views import *


app_name = "Slide"
urlpatterns = [
    path("create/", CreateSlideView.as_view(), name="create_slide"),
    path("update/<int:pk>/", UpdateSlideView.as_view(), name='update_slide')
]
