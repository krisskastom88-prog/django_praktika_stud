# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('supervisor', 'Преподаватель'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True) # <<< СВЯЗЬ С ПОЛЬЗОВАТЕЛЕМ >>>
    full_name = models.CharField(max_length=255)
    group_number = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.full_name
# Модель компании
class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

# Модель практики
class Practice(models.Model):
    STATUS_CHOICES = (
        ('planned', 'Запланирована'),
        ('ongoing', 'Активна'),
        ('completed', 'Завершена'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='practices')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='practices')
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    supervisor_comment = models.TextField(blank=True, null=True)
    grade = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True) # Например, 5.00

    def __str__(self):
        return f"Практика: {self.student.full_name} - {self.company.name}"

# Модель отчёта
class Report(models.Model):
    REPORT_TYPE_CHOICES = (
        ('daily', 'Ежедневный'),
        ('weekly', 'Еженедельный'),
        ('final', 'Итоговый'),
    )

    practice = models.ForeignKey(Practice, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    content = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    reviewed_by_supervisor = models.BooleanField(default=False) # Флаг проверки куратором
    supervisor_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_report_type_display()} отчёт для {self.practice}"