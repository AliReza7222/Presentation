"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

schema_view = get_schema_view (
   openapi.Info(
      title="DynamicPresentationGenerator API",
      default_version='V1',
      description='''Security:

For security, JWT tokens are used for authentication and authorization. Requests are verified using CSRF and only authorized users are allowed access to resources.

Endpoints:

/admin/: Management path for Django admin panel.
/accounts/: Paths related to the authentication module, including user registration and login.
/api/token/refresh/: Path for refreshing JWT tokens.
/api/v1/users/: Paths related to user management.
/api/v1/presentation/: Paths related to slide management.
/api/v1/slide/: Paths related to slide management.
Technical Details:

Django REST Framework is used for creating the API.
drf-yasg is used for generating Swagger documentation.
All requests and responses are in JSON format.
JWT tokens are used for authentication and security.''',
    ),
   public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # allauth
    path('accounts/', include('allauth.urls')),
    # simple jwt token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # app path
    path("api/v1/user/", include("user.urls")),
    path("api/v1/presentation/", include("presentation.urls")),
    path("api/v1/slide/", include("slide.urls")),
    path('api/v1/digikala/', include('digikala.urls')),
    # DRF-YASG URL Configuration
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc'), name='schema-redoc'),
]
