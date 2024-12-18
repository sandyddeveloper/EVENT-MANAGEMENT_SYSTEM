from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('Organizer', 'Organizer'),
        ('Attendee', 'Attendee'),
    )

    email = models.EmailField(unique=True)
    username = None  # Remove username field
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='Attendee')
    is_active = models.BooleanField(default=True)  # Email activation not mandatory for now
    is_attendee = models.BooleanField(default=False)
    is_organizer = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Set a unique related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Set a unique related_name
        blank=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.role})"
