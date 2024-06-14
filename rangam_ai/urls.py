from django.urls import path
from rangam_ai.views import UserView,TokenView,JobDescriptionView
urlpatterns = [
    path('users/',UserView.as_view(),name='users'),
    path('tokens/',TokenView.as_view(),name='tokens'),
    path('job_description/',JobDescriptionView.as_view(),name='job_description'),
]
