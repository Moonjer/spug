from django.urls import path

from .views import *

urlpatterns = [
    path('', BranchView.as_view()),
    path('group/sync', sync_group),
    path('project/sync', sync_project),
]
