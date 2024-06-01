from django.urls import path
from .views import PostJobDescription, TestRecruiterBox

urlpatterns = [
    path('post_jd/', PostJobDescription.as_view(), name='post_job_description'),
    path('test/', TestRecruiterBox.as_view(), name='test_recruiter_box'),
]
