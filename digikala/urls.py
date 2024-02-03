from django.urls import path

from digikala.views import *

app_name = 'digikala'

urlpatterns = [
    path('get_chapters/', GetChaptersView.as_view(), name='get_chapters'),
    path('get_section/', GetSectionView.as_view(), name='get_section')
]
