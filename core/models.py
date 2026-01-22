# core/models.py
# Изменения:
# - Добавлено поле supervisor в Practice (с ограничением по роли 'supervisor')
# - Добавлено поле is_curator в CustomUser (чтобы проще фильтровать кураторов)
# - Улучшены verbose_name и choices
# - Добавлен related_name где нужно

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('supervisor', 'Преподаватель-куратор'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name="Роль")
    is_curator = models.BooleanField(default=False, verbose_name="Является куратором")

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile', verbose_name="Пользователь")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    group_number = models.CharField(max_length=50, verbose_name="Группа")
    email = models.EmailField(blank=True, null=True, verbose_name="Эл. почта")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название предприятия")
    address = models.TextField(blank=True, null=True, verbose_name="Адрес")
    contact_person = models.CharField(max_length=255, blank=True, null=True, verbose_name="Контактное лицо")
    contact_email = models.EmailField(blank=True, null=True, verbose_name="Эл. почта контакта")
    contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон контакта")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предприятие"
        verbose_name_plural = "Предприятия"


class Practice(models.Model):
    STATUS_CHOICES = (
        ('planned', 'Запланирована'),
        ('ongoing', 'В процессе'),
        ('completed', 'Завершена'),
        ('canceled', 'Отменена'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='practices', verbose_name="Студент")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='practices', verbose_name="Предприятие")
    supervisor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'supervisor'},
        related_name='supervised_practices',
        verbose_name="Куратор"
    )
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    description = models.TextField(blank=True, null=True, verbose_name="Описание практики")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned', verbose_name="Статус")
    supervisor_comment = models.TextField(blank=True, null=True, verbose_name="Комментарий куратора")
    grade = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name="Оценка")

    def __str__(self):
        return f"{self.student.full_name} — {self.company.name} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Практика"
        verbose_name_plural = "Практики"


class Report(models.Model):
    REPORT_TYPE_CHOICES = (
        ('daily', 'Ежедневный'),
        ('weekly', 'Еженедельный'),
        ('final', 'Итоговый'),
    )

    practice = models.ForeignKey(Practice, on_delete=models.CASCADE, related_name='reports', verbose_name="Практика")
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, verbose_name="Тип отчёта")
    content = models.TextField(verbose_name="Содержание")
    file = models.FileField(upload_to='reports/%Y/%m/', blank=True, null=True, verbose_name="Прикреплённый файл")
    date_submitted = models.DateTimeField(auto_now_add=True, verbose_name="Дата сдачи")
    reviewed_by_supervisor = models.BooleanField(default=False, verbose_name="Проверено куратором")
    supervisor_feedback = models.TextField(blank=True, null=True, verbose_name="Обратная связь куратора")

    def __str__(self):
        return f"{self.get_report_type_display()} отчёт — {self.practice}"

    class Meta:
        verbose_name = "Отчёт"
        verbose_name_plural = "Отчёты"