from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class Person(models.Model):
    MALE = "M"
    FEMALE = "F"
    DOCUMENT_TYPE = (
        (MALE, "Masculino"),
        (FEMALE, "Femenino"),
    )

    DNI = "DNI"
    ID_CARD = "ID_CARD"
    PASSPORT = "PASSPORT"
    SEX = (
        (ID_CARD, "Cédula"),
        (DNI, "DNI"),
        (PASSPORT, "Pasaporte"),
    )
    first_name = models.CharField(_("Nombres"), max_length=250)
    last_name = models.IntegerField(
        _("Apellidos"),
    )
    document_number = models.IntegerField(_("Número de documento"))
    document_type = models.CharField(
        _("Tipo de documento"),
        choices=DOCUMENT_TYPE,
        max_length=10,
        default=ID_CARD,
    )
    birth_date = models.DateField()
    sexo = models.CharField(
        _("sexo"),
        choices=SEX,
        max_length=10,
        default=MALE,
    )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE, related_name="user", null=True, blank=True
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    rol = models.CharField(
        max_length=30,
        choices=[
            ("patient", "Paciente"),
            ("doctor", "Médico"),
            ("admin", "Administrador"),
        ],
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.username} ({self.email})"


class Contact(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(_("Número de teléfono"), max_length=100, blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Address(models.Model):
    main_street = models.CharField(
        _("Calle principal"),
        max_length=250,
    )
    secondary_stret = models.CharField(_("Calle secundaria"), max_length=250)
    reference = models.CharField(_("Referencia"), max_length=250)
    addrress_number = models.CharField(_("Número de domicilio"), max_length=50)
    city = models.CharField(
        _("Ciudad"),
        max_length=250,
    )
    country = models.CharField(
        _("Pais"),
        max_length=250,
    )
    province = models.CharField(
        _("Provincia"),
        max_length=250,
    )
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)


class Configuration(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    value = models.CharField(
        _("Valor"),
    )
    id_group = models.CharField(
        _("Grupo"),
        max_length=100,
    )
    is_delete = models.BooleanField()


class Menu(models.Model):
    key = models.CharField(_("Key"), max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="children"
    )
    groups = models.ManyToManyField(
        Group, blank=True, help_text="Roles que pueden ver este menú"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.key


class Translation(models.Model):
    key = models.CharField(max_length=200)
    language = models.CharField(max_length=10, choices=settings.LANGUAGES)
    text = models.TextField()

    class Meta:
        unique_together = ("key", "language")

    def __str__(self):
        return f"{self.key} ({self.language})"
