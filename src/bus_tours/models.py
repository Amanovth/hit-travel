from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.conf import settings


class Meals(models.Model):
    name = models.CharField(max_length=5)
    fullname = models.CharField(max_length=255)
    russian = models.CharField(max_length=255)
    russianfull = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name} - {self.russian}"

    class Meta:
        verbose_name = _("Питание")
        verbose_name_plural = _("Питание")


class Category(models.Model):
    name = models.CharField(_("Название"), max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")


class BusTours(models.Model):
    DEPARTURE_CHOICES = (
        ("Ташкент", "Ташкент"),
        ("Бишкек", "Бишкек"),
        ("Баку", "Баку"),
    )

    cat = models.ForeignKey(Category, verbose_name=_("Категория"), default=1, on_delete=models.CASCADE)
    title = models.CharField(_("Заголовок"), max_length=255)
    country = models.CharField(_("Страна"), max_length=255, default="")
    departure = models.CharField(
        _("Откуда"), max_length=255, choices=DEPARTURE_CHOICES, default="Бишкек"
    )
    num_of_tourists = models.IntegerField(_("Количество туристов"), default=2)
    seats = models.IntegerField(_("Доступно мест"))
    datefrom = models.DateField(_("Начало тура"))
    dateto = models.DateField(_("Окончание тура"))
    nights = models.IntegerField(_("Ночей"))
    days = models.IntegerField(_("Дней"))
    meal = models.ForeignKey(
        Meals, verbose_name=_("Питание"), on_delete=models.SET_DEFAULT, default=1
    )
    price = models.IntegerField(_("Цена"))
    description = RichTextField(_("Описание"))
    description_pdf = models.FileField(
        _("Описание тура PDF"), upload_to="descriptions", null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.title} {self.nights} ночей"

    class Meta:
        verbose_name = _("Автобусный тур")
        verbose_name_plural = _("Автобусные туры")


class TourProgram(models.Model):
    tour = models.ForeignKey(
        BusTours, on_delete=models.CASCADE, related_name="programs"
    )
    day = models.IntegerField(_("День"))
    title = models.CharField(_("Заголовок"), max_length=255)
    body = RichTextField(_("Тело"))

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Программа")
        verbose_name_plural = _("Программа")


class TourCondition(models.Model):
    tour = models.ForeignKey(
        BusTours, on_delete=models.CASCADE, related_name="conditions"
    )
    title = models.CharField(_("Заголовок"), max_length=255)
    body = RichTextField(_("Тело"))

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Условие тура")
        verbose_name_plural = _("Условие тура")


class TourExcursions(models.Model):
    tour = models.ForeignKey(
        BusTours, on_delete=models.CASCADE, related_name="excursions"
    )
    title = models.CharField(_("Заголовок"), max_length=255)
    body = RichTextField(_("Тело"))

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Экскурсия")
        verbose_name_plural = _("Экскурсии")


class Cities(models.Model):
    tour = models.ForeignKey(BusTours, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField((_("Название города")))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Город")
        verbose_name_plural = _("Города")


class Gallery(models.Model):
    tour = models.ForeignKey(BusTours, on_delete=models.CASCADE, related_name="gallery")
    img = models.ImageField(_("Изображение"), upload_to="gallery")

    def __str__(self) -> str:
        return ""

    class Meta:
        verbose_name = _("Изображение")
        verbose_name_plural = _("Галерея")


class Reviews(models.Model):
    tour = models.ForeignKey(BusTours, on_delete=models.CASCADE, related_name="reviews")
    full_name = models.CharField(_("ФИО"), max_length=255)
    email = models.EmailField(_("Email"))
    body = models.TextField(_("Отзыв"))
    created_at = models.DateTimeField(_("Дата отзыва"), auto_now_add=True)

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")


class BusTourRequest(models.Model):
    PAYMENT_STATUS_CHOICES = (
        (1, "Не оплачена"),
        (2, "Частично оплачена"), 
        (3, "Полностью оплачена"),
    )
    
    STATUS_CHOICES = (
        (1, "Новая"),
        (2, "В работе"), 
        (3, "Подтверждена"),
    )
    
    GENDER_CHOICES = (
        ("Муж", "Муж"),
        ("Жен", "Жен")
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    tour = models.ForeignKey(BusTours, on_delete=models.SET_NULL, null=True, related_name="bus_tour_request")
    status = models.IntegerField(_("Статус"), default=1, choices=STATUS_CHOICES)
    payment_status = models.IntegerField(_("Статус оплаты"), default=1, choices=PAYMENT_STATUS_CHOICES)
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
    
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
        
    class Meta:
        verbose_name = _("Заявка")
        verbose_name_plural = _("Заявки")
        
    
class Travelers(models.Model):
    GENDER_CHOICES = (
        ("Муж", "Муж"),
        ("Жен", "Жен")
    )
    
    main = models.ForeignKey(BusTourRequest, on_delete=models.CASCADE, related_name="bustour_travelers")
    dateofborn = models.DateField(_("Дата рождения"))
    first_name = models.CharField(_("Имя"), max_length=100)
    last_name = models.CharField(_("Фамилия"), max_length=100)
    gender = models.CharField(_("Пол"), choices=GENDER_CHOICES, max_length=3)
        
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("Путешественник")
        verbose_name_plural = _("Путешественники")