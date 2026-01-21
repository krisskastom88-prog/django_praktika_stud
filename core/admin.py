# core/admin.py

from django.contrib import admin
from .models import CustomUser, Student, Company, Practice, Report

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'group_number', 'email', 'phone')
    search_fields = ('full_name', 'group_number')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'contact_email', 'contact_phone')
    search_fields = ('name', 'contact_person')

@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    list_display = ('student', 'company', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('student__full_name', 'company__name')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('practice', 'report_type', 'date_submitted', 'reviewed_by_supervisor')
    list_filter = ('report_type', 'reviewed_by_supervisor', 'date_submitted')
    search_fields = ('practice__student__full_name', 'content')