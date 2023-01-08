from django.urls import path
from .views import Perks, PerkDetail
from . import views


urlpatterns = [
    path("", views.Experiences.as_view()),  # x
    path("<int:ex_pk>", views.ExperienceDetail.as_view()),  # GET PUT DELETE
    path("<int:ex_pk>/bookings", views.ExperBooking.as_view()),  #
    path(
        "<int:ex_pk>/bookings/<int:book_pk>", views.ExperienceBookingRevise.as_view()
    ),  # GET put delete
    path("perks/", views.Perks.as_view()),
    path("perks/<int:pk>", views.PerkDetail.as_view()),
]
