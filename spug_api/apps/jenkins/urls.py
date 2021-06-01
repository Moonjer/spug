from django.urls import path

from .views import *

urlpatterns = [
    path('job', JobView.as_view()),
    path('job/sync', sync_jobs),
]
