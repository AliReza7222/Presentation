from django.conf import settings
from django.urls import include, path
from rest_framework import routers

from .views import SlideViewSet


if settings.DEBUG:
    router = routers.DefaultRouter()
else :
    router = routers.SimpleRouter()
router.register(r'', SlideViewSet, basename='slide_viewset')

app_name = "Slide"
urlpatterns = router.urls
