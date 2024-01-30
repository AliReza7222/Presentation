from django.urls import path

from presentations.api.v1.views import *

app_name = "presentations"

urlpatterns = [
    path("create/", CreatePresentationView.as_view(), name='create_presentation'),
    path("create/tag/", CreateTagView.as_view(), name="create_tag"),
    path("update/<int:pk>/", UpdatePresentationView.as_view(), name='update_presentation'),
    path("update/tag/<int:pk>/", UpdateTagView.as_view(), name='update_tag'),
    path("delete/<int:pk>/", DeletePresentationView.as_view(), name="delete_presentation"),
    path("delete/tag/<int:pk>/", DeleteTagView.as_view(), name="delete_tag")
]
