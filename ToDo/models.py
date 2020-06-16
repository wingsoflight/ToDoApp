from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _
from ToDoApp.tasks import on_task_changed


# Create your models here.

class AppUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class AppUser(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('Email'), unique=True)
    REQUIRED_FIELDS = []
    objects = AppUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.email = self.username
        super(AppUser, self).save(*args, **kwargs)


class Task(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    deadline = models.DateTimeField(blank=False)
    completed = models.BooleanField(default=False)
    __completed = None

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.__completed = self.completed

    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
        if self.__completed != self.completed:
            task = on_task_changed.delay(self.id, self.completed)