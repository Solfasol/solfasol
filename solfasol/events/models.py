from django.db import models


class EventType(models.Model):
    name = models.CharField("Tip", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Etkinlik tipi"
        verbose_name_plural = "Etkinlik tipleri"


class Event(models.Model):
    title = models.CharField("Başlık", max_length=200)
    type = models.ForeignKey(EventType, blank=True, null=True, on_delete=models.SET_NULL)
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
    active = models.BooleanField("Aktif", default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('start',)
        verbose_name = "Etkinlik"
        verbose_name_plural = "Etkinlikler"
