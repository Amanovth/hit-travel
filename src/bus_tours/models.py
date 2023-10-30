from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


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
