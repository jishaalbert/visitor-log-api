from django.urls import path
from . import views

urlpatterns = [
    path('checkin/', views.check_in),
    path('checkout/', views.check_out),
    path('inside/', views.visitors_inside),
    path('by-date/', views.visitors_by_date),
    path('search/', views.search_visitors),
]
