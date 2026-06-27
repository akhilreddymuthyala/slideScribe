from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    avatar_initials = models.CharField(max_length=3, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if self.full_name:
            parts = self.full_name.strip().split()
            if len(parts) >= 2:
                self.avatar_initials = (parts[0][0] + parts[-1][0]).upper()
            elif len(parts) == 1:
                self.avatar_initials = parts[0][:2].upper()
        elif self.email:
            self.avatar_initials = self.email[:2].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email