from django.urls import path

from .views import *


app_name = 'user'
urlpatterns = [
    path('register/', SignUpUserView.as_view(), name="register"),
    path('login/', SignInUserView.as_view(), name='login'),
    path('profile/update/<int:pk>/', UpdateProfileUserView.as_view(), name='update_profile'),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    path('reset_password/', ResetPasswordView.as_view(), name="reset_password"),
]
