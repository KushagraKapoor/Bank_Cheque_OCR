
from django.urls import path
from .views import CheckUploadView, CheckResultView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', CheckUploadView.as_view(), name='check_upload'),
    path('result/<int:pk>/', CheckResultView.as_view(), name='check_result'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


