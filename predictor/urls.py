from django.urls import path
from .views import predict, home, predict_dish

urlpatterns = [
    path('', home),
    path('predict/', predict),
    path('predict_dish/', predict_dish),   # NEW LINE
]