from django.db import models
from django.contrib.auth.models import User


class Service(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    mini_description = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class Rate_Name(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["id"]
        verbose_name = "Название тарифа"
        verbose_name_plural = "Названия тарифов"


class Rate(models.Model):
    service = models.ForeignKey(Service, related_name="rates", on_delete=models.CASCADE)
    name = models.ForeignKey(Rate_Name, related_name="rates", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"{self.service.name} - {self.name} - {self.price}₽"

    class Meta:
        ordering = ["id"]
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"


class Application_Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус заявки"
        verbose_name_plural = "Статусы заявок"


class Application(models.Model):
    status = models.ForeignKey(
        Application_Status, on_delete=models.CASCADE, related_name="applications"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    formed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    user_creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_applications"
    )
    moderator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="moderated_applications",
    )

    def __str__(self):
        return f"Заявка {self.id} - {self.status.name}"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]


class Application_Service(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="services"
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="applications"
    )

    class Meta:
        unique_together = ("application", "service")
        verbose_name = "Услуга в заявке"
        verbose_name_plural = "Услуги в заявке"

    def __str__(self):
        return f"Заявка {self.application.id} - Услуга {self.service.name}"
