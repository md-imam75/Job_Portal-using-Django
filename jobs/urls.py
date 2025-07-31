from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='home'),
    path('post/', views.post_job, name='post_job'),
    path('my_jobs/', views.my_jobs, name='my_jobs'),
    path('job/<int:job_id>/applicants/', views.applicants, name='applicants'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('my_applications/', views.my_applications, name='my_applications'),
]