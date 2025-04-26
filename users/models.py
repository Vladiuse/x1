from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from users.utils import generate_reset_password_code
from datetime import datetime, timedelta
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email: str, password: str, **extra_fields) -> 'CustomUser':
        if not email:
            raise ValueError('Email field required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> 'CustomUser':
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class ResetUserPasswordCodeManager(models.Manager):
    def create_for_user(self, user: CustomUser) -> 'ResetUserPasswordCode':
        return self.create(
            user=user,
            email=user.email,
            reset_password_code=generate_reset_password_code(),
            expire_date=timezone.now() + timedelta(hours=1),
        )

class ResetUserPasswordCode(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    reset_password_code = models.CharField(max_length=6)
    expire_date = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    objects = ResetUserPasswordCodeManager()
