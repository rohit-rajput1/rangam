from django.urls import path
from .views import post_job_description

urlpatterns = [
    path('post_job_description/', post_job_description, name='post_job_description'),
]

