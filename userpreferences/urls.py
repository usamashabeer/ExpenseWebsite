from django.urls import path, include

from .views import UserPreferences

urlpatterns = [
    path('preferences',UserPreferences.as_view(),name='preferences'),
]