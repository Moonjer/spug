from django.urls import path

from .views import *

urlpatterns = [
    path('', BranchView.as_view()),
]
