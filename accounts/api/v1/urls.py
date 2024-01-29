from django.urls import path

from accounts.api.v1.views import SignUpUserView, SignInUserView


app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUpUserView.as_view(), name="sign_up"),
    path('signin/', SignInUserView.as_view(), name='sign_in')
]
