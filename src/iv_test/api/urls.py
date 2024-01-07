from django.urls import path

from . import views

app_name = 'api'

# routing
urlpatterns = [
    path('analysis', views.analysis, name="analysis"),
]
