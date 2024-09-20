from django.urls import path

from .views import ImageViewSet

urlpatterns = [
    path('image/', ImageViewSet.as_view(), name='upload'),
]
