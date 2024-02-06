from django.urls import path

from .views import *


app_name = 'accounts'
urlpatterns = [
    path('register/', SignUpUserView.as_view(), name="sign_up"),
    path('login/', SignInUserView.as_view(), name='sign_in'),
    path('update/profile/', UpdateProfileUserView.as_view(), name='update_profile'),
]
