from datetime import timedelta, datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import get_template
import pdfkit
from num2words import num2words

from ..base.services import get_path_upload_photo, validate_size_image
from .services import add_tourist_on_user_creation, add_lead_on_creation


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required for users")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    balance = models.DecimalField(_("Balance"), default=0, max_digits=10, decimal_places=2)
    bonuses = models.DecimalField(_("Bonuses"), default=0, max_digits=10, decimal_places=2)
    email = models.EmailField(_("Email"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    is_verified = models.BooleanField(_("Verification"), default=False)
    phone = models.CharField(verbose_name=_("Телефон"), max_length=100)
    verification_code = models.IntegerField(_("Verification code"), null=True, blank=True)
    verification_code_time = models.DateTimeField(_("Verification code created time"), null=True, blank=True)
    password_reset_token = models.CharField(_("Password Reset"), max_length=100, blank=True, null=True, unique=True)
    photo = models.ImageField(
        _("Аватар"), 
        upload_to=get_path_upload_photo,
        default="default.png",
        validators=[validate_size_image],
    )
    date_birth = models.DateField(_("Дата рождения"), null=True, blank=True)
    
    inn = models.CharField(_("ИНН"), max_length=100, null=True, blank=True)
    date_of_issue = models.DateField(_("Дата выдачи"), null=True, blank=True)
    issued_by = models.CharField(_("Орган выдачи"), null=True, blank=True)
    validity = models.DateField(_("Срок действия"), null=True, blank=True)
    city = models.CharField(_("Город"), max_length=255, null=True, blank=True)
    passport_front = models.ImageField(_("Фото паспорта, передняя сторона"), upload_to="passports", null=True, blank=True)
    passport_back = models.ImageField(_("Фото паспорта, задняя сторона"), upload_to="passports",null=True, blank=True)
    passport_id = models.CharField(_("ID паспорта"), max_length=8, null=True, blank=True, unique=True)
    county = models.CharField(_("Страна"), max_length=100, null=True, blank=True)
    tourist_id = models.IntegerField(_("ID Туриста"), null=True, blank=True)
    manager_id = models.IntegerField(_("ID менеджера"), null=True, blank=True)
    bcard_number = models.CharField(_("Номер бонусного счёта"), max_length=255, null=True, blank=True)
    bcard_id = models.IntegerField(_("ID бонусного счёта"), null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.bcard_number = str(100).zfill(10)

@receiver(post_save, sender=User)
def add_tourist(sender, instance, created, **kwargs):
    if created:
        add_tourist_on_user_creation(sender, instance)


class BonusHistory(models.Model):
    CURRENCY_CHOICES = (
        ("СОМ", "СОМ"),
        ("USD", "USD")
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bonus_history")
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
    STATUS_CHOICES = (
        (1, "Новая заявка"),
        (2, "В процессе покупки"),
        (3, "Тур куплен"),
        (4, "Отклонено"),
    )
    
    user = models.ForeignKey(User, verbose_name=_("Пользователь"), on_delete=models.CASCADE)
    status = models.IntegerField(_("Статус"), choices=STATUS_CHOICES, default=2)
    request_number = models.IntegerField(_("Номер заявки"), null=True, blank=True)
    
    first_name = models.CharField(_("Имя"), max_length=100)
    last_name = models.CharField(_("Фамилия"), max_length=100)
    phone = models.CharField(_("Телефон"), max_length=100)
    email = models.EmailField(_("E-mail"), max_length=100)
    gender = models.CharField(_("Пол"), choices=GENDER_CHOICES, max_length=3)
    dateofborn = models.DateField(_("Дата рождения"))
    
    # Passport Info
    inn = models.CharField(_("ИНН"), max_length=100)
    passport_id = models.CharField(_("ID пасспорта"), max_length=255)
    date_of_issue = models.DateField(_("Дата выдачи"))
    issued_by = models.CharField(_("Орган выдачи"))
    validity = models.DateField(_("Срок действия"))
    city = models.CharField(_("Город"), max_length=255)
    country = models.CharField(_("Страна"), max_length=255)
    passport_front = models.ImageField(_("Фото паспорта, передняя сторона"), upload_to="passports", null=True, blank=True)
    passport_back = models.ImageField(_("Фото паспорта, задняя сторона"), upload_to="passports",null=True, blank=True)
    
    operatorlink = models.URLField(_("Ссылка на оператора"), max_length=1000)
    price = models.CharField(_("Цена"), max_length=255, null=True, blank=True)
    currency = models.CharField(_("Валюта"), max_length=255, null=True, blank=True)
    tourid = models.CharField(_("Код тура"), max_length=100)
    bonuses = models.DecimalField(_("Бонусы"), default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True, null=True, blank=True)
    surcharge = models.CharField(_("Доплата"), max_length=255, default=10)
    agreement = models.FileField(_("Договор"), upload_to="agreements", null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        super(TourRequest, self).save(*args, **kwargs)
    
    def deadline(self):
        deadline = self.created_at + timedelta(days=10)
        return deadline.strftime('%d.%m.%Y %H:%M')
        
    class Meta:
        verbose_name = _("Заявка")
        verbose_name_plural = _("Заявки")


@receiver(post_save, sender=TourRequest)
def add_request(sender, instance, created, **kwargs):
    if created:
        add_lead_on_creation(sender, instance)


class Documents(models.Model):
    request = models.ForeignKey(TourRequest, on_delete=models.CASCADE, related_name="documents")
    name = models.CharField(_("Название документа"), max_length=255, null=True, blank=True)
    file = models.FileField(_("Документ"), upload_to="documents")
    created_at = models.DateField(_("Дата создания"), auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    
    class Meta:
        verbose_name = _("Документ")
        verbose_name_plural = _("Прикрепленные документы")
    
    
    
class Travelers(models.Model):
    GENDER_CHOICES = (
        ("Муж", "Муж"),
        ("Жен", "Жен")
    )
    
    main = models.ForeignKey(TourRequest, on_delete=models.CASCADE, related_name="travelers")
    dateofborn = models.DateField(_("Дата рождения"))
    first_name = models.CharField(_("Имя"), max_length=100)
    last_name = models.CharField(_("Фамилия"), max_length=100)
    gender = models.CharField(_("Пол"), choices=GENDER_CHOICES, max_length=3)
        
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("Путешественник")
        verbose_name_plural = _("Путешественники")

    
class Payments(models.Model):
    img = models.ImageField(_("QRCode"), upload_to="payments")
    description = RichTextField(_("Инструкция"), max_length=255)
    bank_name = models.CharField(_("Название банка"), null=True, blank=True)
    icon = models.ImageField(_("Иконка"), upload_to="payments", null=True, blank=True)
    
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        
    def __str__(self):
        return self.bank_name
    

class FAQ(models.Model):
    question = models.CharField(_("Вопрос"), max_length=255)
    answer = RichTextField(_("Ответ"))
    
    def __str__(self) -> str:
        return self.question
    
    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQ")


