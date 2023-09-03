from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from ..base.services import get_path_upload_photo, validate_size_image


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required for users')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    balance = models.DecimalField(_('Balance'), default=0, max_digits=10, decimal_places=2)
    bonuses = models.DecimalField(_('Bonuses'), default=0, max_digits=10, decimal_places=2)
    email = models.EmailField(_('Email'))
    is_verified = models.BooleanField(_('Verification'), default=False)
    phone = models.CharField(verbose_name=_('Phone'), max_length=12, unique=True, null=True, blank=True)
    verification_code = models.IntegerField(_('Verification code'), null=True, blank=True)
    verification_code_time = models.DateTimeField(_('Verification code created time'), null=True, blank=True)
    password_reset_token = models.CharField(_('Password Reset'), max_length=100, blank=True, null=True, unique=True)
    photo = models.ImageField(
        _('Profile photo'), 
        upload_to=get_path_upload_photo,
        default='default_profile_photo.png',
        validators=[validate_size_image],
    )
    date_birth = models.DateField(_('Date of birth'), null=True, blank=True)
    passport_id = models.CharField(_('Passport ID'), max_length=8, null=True, blank=True, unique=True)
    county = models.CharField(_('Country'), max_length=100, null=True, blank=True)
    tourist_id = models.IntegerField(_('ID Туриста'), null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        
    def __str__(self):
        return self.email
    

class OrdeerHistory(models.Model):
    pass