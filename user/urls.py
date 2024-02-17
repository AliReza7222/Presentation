from django.urls import path

from .views import *


app_name = 'user'
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name="register"),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/update/', UpdateProfileUserView.as_view(), name='update_profile'),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    path('reset_password/', ResetPasswordView.as_view(), name="reset_password"),
    path('active_account/', ActiveUserView.as_view(), name="active_account")
]
