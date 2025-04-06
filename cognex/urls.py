from django.urls import path

from .views import onResult

urlpatterns = [
    path('onResult/', onResult, name='onResult'),
    # path('events/', sse_view, name='events'),
]
