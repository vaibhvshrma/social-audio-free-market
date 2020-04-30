from django.urls import path
from .views import *

urlpatterns = [
    path('api/quick', QuickSearch.as_view()),
    path('api/sample/<int:sample_id>', SamplePage.as_view()),
    path('api/sample_file/<int:sample_id>', SampleFile.as_view()),
    path('api/profile/<int:user_id>', UserProfilePage.as_view()),
    path('api/samples/<int:user_id>', UserSamples.as_view()),
]