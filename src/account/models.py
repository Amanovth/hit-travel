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
    email = models.EmailField(_('Email'), unique=True)
    is_verified = models.BooleanField(_('Verification'), default=False)
    phone = models.CharField(verbose_name=_('Phone'), max_length=12, null=True, blank=True)
    verification_code = models.IntegerField(_('Verification code'), null=True, blank=True)
    verification_code_time = models.DateTimeField(_('Verification code created time'), null=True, blank=True)
    password_reset_token = models.CharField(_('Password Reset'), max_length=100, blank=True, null=True, unique=True)
    photo = models.ImageField(
        _('Profile photo'), 
        upload_to=get_path_upload_photo,
        default='default.png',
        validators=[validate_size_image],
    )
    date_birth = models.DateField(_('Date of birth'), null=True, blank=True)
    passport_id = models.CharField(_('Passport ID'), max_length=8, null=True, blank=True, unique=True)
    county = models.CharField(_('Country'), max_length=100, null=True, blank=True)
    tourist_id = models.IntegerField(_('ID Туриста'), null=True, blank=True)
    manager_id = models.IntegerField(_('ID менеджера'), null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        
    def __str__(self):
        return self.email
    

class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_history')
    tourid = models.CharField(_('Код тура'), max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(_('Дата заказа'), auto_now_add=True, null=True, blank=True)
    sum = models.CharField(_('Сумма заказа'), max_length=100, null=True, blank=True)
    flydate = models.DateField(_('Дата вылета'), null=True, blank=True)
    nights = models.CharField(_('Ночи'), max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    
    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name = _("История заказов")
        verbose_name_plural = _("История заказов")


class BonusHistory(models.Model):
    CURRENCY_CHOICES = (
        ("СОМ", "СОМ"),
        ("USD", "USD")
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bonus_history')
    name = models.CharField(_("Название бонуса"), max_length=255)
    created_at = models.DateTimeField(_("Дата"))
    valid = models.DateField(_("Действителен до"))
    sum = models.IntegerField(_("Сумма"), default=0)
    currency = models.CharField(_("Валюта"), choices=CURRENCY_CHOICES, max_length=5, default="СОМ")
    
    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name  = _("История бонусов")
        verbose_name_plural = _("История бонусов")
        
        
class TourRequest(models.Model):
    GENDER_CHOICES = (
        ("Муж", "Муж"),
        ("Жен", "Жен")
    )
    
    user = models.ForeignKey(User, verbose_name=_("Пользователь"), on_delete=models.CASCADE)
    first_name = models.CharField(_("Имя"), max_length=100)
    last_name = models.CharField(_("Фамилия"), max_length=100)
    phone = models.CharField(_("Телефон"), max_length=100)
    email = models.EmailField(_("E-mail"), max_length=100)
    gender = models.CharField(_("Пол"), choices=GENDER_CHOICES, max_length=3)
    citizenship = models.CharField(_("Гражданство"), max_length=100)
    inn = models.CharField(_("ИНН"), max_length=100)
    tourid = models.CharField(_("Код тура"), max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = _("Заявка")
        verbose_name_plural = _("Заявки")
    
    
class Payments(models.Model):
    img = models.ImageField(_("QRCode"), upload_to='payments')
    full_name = models.CharField(_("Имя получателя"), max_length=255)
    bank_name = models.CharField(_("Название банка"), null=True, blank=True)
    icon = models.ImageField(_("Иконка"), upload_to='payments', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        
    def __str__(self):
        return self.full_name