from django.urls import path

from .views import *

urlpatterns = [
    path('branch', BranchView.as_view()),
    path('project', ProjectView.as_view()),
    path('group/sync', sync_group),
    path('project/sync', sync_project),
    path('branch/sync', sync_branch),
]
