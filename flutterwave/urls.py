from django.urls import path
from . import views

urlpatterns = [
    path( 'register/', views.RegisterView.as_view()),
    path( 'login/', views.LoginView.as_view()),
    path( 'go-premium/', views.PaymentPlanView.as_view()),
    path( 'users-list/', views.ViewUsers.as_view()),
]