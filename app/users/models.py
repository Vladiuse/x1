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
    MAX_ATTEMPTS = 3

    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    reset_password_code = models.CharField(max_length=6)
    expire_date = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    verified_expire_date = models.DateTimeField(null=True, default=None)
    attempts = models.PositiveIntegerField(default=0)
    is_password_reset = models.BooleanField(default=False)

    is_deactivated = models.BooleanField(default=False)

    objects = ResetUserPasswordCodeManager()

    def check_code(self, code: str) -> tuple[bool, str]:
        if self.is_verified:
            return False, 'Code already verified'
        if timezone.now() > self.expire_date:
            return False, 'Code expired'
        if self.reset_password_code == code:
            self.verify()
            return True, "Code verified successfully."
        self.attempts += 1
        self.save()
        if self.attempts >= self.MAX_ATTEMPTS:
            return False, 'Too many failed attempts.'
        return False, 'Wrong code'

    def verify(self) -> None:
        self.is_verified = True
        self.verified_expire_date = timezone.now() + timedelta(minutes=10)
        self.save()

    def is_password_can_be_reset(self) -> bool:
        if not self.is_verified:
            return False
        if timezone.now() > self.verified_expire_date:
            return False
        return not self.is_password_reset

    def mark_password_reset(self) -> None:
        self.is_password_reset = True
        self.save()

    def deactivate(self) -> None:
        self.is_deactivated = True
        self.save()