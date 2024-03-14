from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('diagnose/', views.dashboard, name='prediction-page'),
    path('result/', RedirectView.as_view(url='/diagnose/result/', permanent=False)),
    path('diagnose/result/', views.model_predictor, name='result'),
]
