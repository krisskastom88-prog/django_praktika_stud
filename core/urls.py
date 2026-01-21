# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.students_list, name='students_list'),
    path('companies/', views.companies_list, name='companies_list'),
    path('practices/', views.practices_list, name='practices_list'),
    path('reports/', views.reports_list, name='reports_list'),

    path('students/add/', views.add_student, name='add_student'),
    path('companies/add/', views.add_company, name='add_company'),
    # ... (другие маршруты для добавления/редактирования)

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # ... (другие маршруты)
]