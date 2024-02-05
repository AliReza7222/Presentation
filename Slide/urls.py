from django.urls import include, path
from rest_framework import routers

from Slide.views import SlideViewSet


router = routers.DefaultRouter()
router.register(r'', SlideViewSet, basename='slide_viewset')

app_name = "Slide"
urlpatterns = router.urls
