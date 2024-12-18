from django.urls import path
from .views import ExecuteCommandAPIView

urlpatterns = [
    path('execute-command/', ExecuteCommandAPIView.as_view(), name='execute-command'),
]
