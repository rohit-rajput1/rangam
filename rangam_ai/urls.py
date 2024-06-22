from django.urls import path
from rangam_ai.views import UserView,TokenView,JobDescriptionView,JobSkillsRequiredView, JobQuestionsRequiredView, JobKeyResponsibilitiesRequiredView
urlpatterns = [
    path('users/',UserView.as_view(),name='users'),
    path('tokens/',TokenView.as_view(),name='tokens'),
    path('job_description/',JobDescriptionView.as_view(),name='job_description'),
    path('job-skills-required/', JobSkillsRequiredView.as_view(), name='job-skills-required'),
    path('job-questions-required/', JobQuestionsRequiredView.as_view(), name='job-questions-required'),
    path('job-key-responsibilities-required/', JobKeyResponsibilitiesRequiredView.as_view(), name='job-key-responsibilities-required'),
]