# core/admin.py
# Изменения:
# - Добавлены все поля в list_display
# - Добавлены фильтры и поиск по связанным моделям
# - Добавлен inlines для Report в Practice

from django.contrib import admin
from .models import CustomUser, Student, Company, Practice, Report


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_curator', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_curator', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'group_number', 'user__username', 'email', 'phone')
    search_fields = ('full_name', 'group_number', 'user__username', 'email')
    list_filter = ('group_number',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'contact_email', 'contact_phone')
    search_fields = ('name', 'contact_person', 'contact_email')


class ReportInline(admin.TabularInline):
    model = Report
    extra = 1
    fields = ('report_type', 'date_submitted', 'reviewed_by_supervisor', 'file')


@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    list_display = ('student', 'company', 'supervisor', 'start_date', 'end_date', 'status', 'grade')
    list_filter = ('status', 'start_date', 'end_date', 'supervisor', 'company')
    search_fields = ('student__full_name', 'company__name', 'supervisor__username')
    inlines = [ReportInline]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('practice', 'report_type', 'date_submitted', 'reviewed_by_supervisor', 'file')
    list_filter = ('report_type', 'reviewed_by_supervisor', 'date_submitted')
    search_fields = ('practice__student__full_name', 'content')
    readonly_fields = ('date_submitted',)