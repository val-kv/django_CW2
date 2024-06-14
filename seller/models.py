from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User


class Newsletter(models.Model):
    PERIODICITY_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('daily', 'Daily'),
    ]
    title = models.CharField(max_length=100)
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('sent', 'Sent'), ('scheduled', 'Scheduled')])
    groups = models.ManyToManyField('auth.Group', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='newsletters', default=1)
    periodicity = models.CharField(max_length=20, choices=PERIODICITY_CHOICES, default='weekly')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-sent_date']
        permissions = [
            ('custom_view_newsletter', 'Может просматривать любой новостной бюллетень'),
            ('view_users', 'Может просматривать список пользователей сервиса'),
            ('block_users', 'Может заблокировать пользователей сервиса'),
            ('disable_newsletter', 'Может отключить новостные бюллетени'),
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.owner = self.owner or self.request.user
        super().save(*args, **kwargs)


class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    subject = models.CharField(max_length=100, default='')  # Добавлено поле для темы письма
    body = models.TextField(default='')  # Добавлено поле для тела письма

    def save(self, *args, **kwargs):
        if not self.pk:
            self.owner = self.owner or self.request.user
        super().save(*args, **kwargs)


class Client(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.owner = self.owner or self.request.user
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
