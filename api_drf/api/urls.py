from django.urls import path
from .views import HashPasswordView, VerifyPasswordView

urlpatterns = [
    path('hash/', HashPasswordView.as_view(), name='hash'),
    path('verify/', VerifyPasswordView.as_view(), name='verify')
]