from django.urls import path

from .views import SlotBooking

urlpatterns = [
    path('',SlotBooking.as_view())
]