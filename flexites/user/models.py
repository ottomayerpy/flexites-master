from django.db import models


class Organization(models.Model):
    fullname = models.CharField(max_length=255, unique=True,
                            verbose_name="Наименование")
    shortname = models.CharField(max_length=255, unique=True,
                            verbose_name="Краткое наименование")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class FlexUser(models.Model):
    email = models.CharField(max_length=255, verbose_name="Почта", unique=True)
    password = models.CharField(max_length=255, verbose_name="Пароль")
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    firstname = models.CharField(max_length=255, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    organizations = models.ManyToManyField(
        Organization, verbose_name="Организация")

    def __str__(self):
        return self.surname

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
