from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User


class Newsletter(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('sent', 'Sent'), ('scheduled', 'Scheduled')])
    groups = models.ManyToManyField('auth.Group', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='newsletters', default=1)

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


class Client(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.owner = self.owner or self.request.user
        super().save(*args, **kwargs)


class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.owner = self.owner or self.request.user
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='media/')
    views = models.IntegerField(default=0)
    publish_date = models.DateTimeField(auto_now_add=True)