from django.contrib.auth.models import AbstractUser, Group, User, Permission
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users')

    def __str__(self):
        return self.username


class ManagerGroup(Group):
    class Meta:
        permissions = [
            ('custom_view_newsletter', 'Может просматривать любой новостной бюллетень'),
            ('view_users', 'Может просматривать список пользователей сервиса'),
            ('block_users', 'Может заблокировать пользователей сервиса'),
            ('disable_newsletter', 'Может отключить новостные бюллетени'),
        ]

    def save(self, *args, **kwargs):
        self.name = 'Manager'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name