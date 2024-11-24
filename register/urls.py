# register/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import RegisterView, VerifyEmailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
]

if settings.DEBUG:  # Faqat DEBUG rejimida ishlaydi
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)