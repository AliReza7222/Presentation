from django.urls import path

from .views import *

app_name = 'digikala'

urlpatterns = [
    path('get_chapters/', GetChaptersView.as_view(), name='get_chapters'),
    path('get_section/', GetSectionView.as_view(), name='get_section'),
    path('section_by_link/', GetSectionByLinkView.as_view(), name='get_section_by_link')
]
