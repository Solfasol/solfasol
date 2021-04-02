from django.db import models


class Event(models.Model):
    title = models.CharField("Başlık", max_length=200)
    start = models.DateTimeField("Başlangıç")
    end = models.DateTimeField("Bitiş", blank=True, null=True)
    description = models.TextField("Tanım", blank=True, null=True)
    address = models.CharField(
        "Adres", max_length=400, blank=True, null=True,
        help_text="Online etkinlikler için toplantı URL'i",
    )
    online = models.BooleanField(default=False)
    link = models.URLField(
        blank=True, null=True,
        help_text="Detaylı bilgi için bağlantı",
    )

    class Meta:
        verbose_name = "Etkinlik"
        verbose_name_plural = "Etkinlikler"
