from django.urls import path

from accounts.api.v1.views import *


app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUpUserView.as_view(), name="sign_up"),
    path('signin/', SignInUserView.as_view(), name='sign_in'),
    path('update/profile/<int:pk>/', UpdateProfileUserView.as_view(), name='update_profile'),
]
