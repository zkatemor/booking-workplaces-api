from django.urls import path

from booking_workplaces_api import views

app_name = "booking_workplaces_api"

urlpatterns = [
    path("workplaces", views.WorkplaceView.as_view()),
]
