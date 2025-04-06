from django.urls import path

from .views import index, sse_view

urlpatterns = [
    path('', index, name='index'),
    path('events/', sse_view, name='events'),
]
