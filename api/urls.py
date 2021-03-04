from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('trades', views.TradeList.as_view()),
    path('trades/<int:pk>', views.TradeDetail.as_view()),
    path('portfolio', views.PortfolioView.as_view()),
    path('returns', views.ReturnsView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)