from django.urls import path

from .views import SlotBooking, welcome_view

urlpatterns = [
    path('', welcome_view),
    path('slot', SlotBooking.as_view()),
]