from django.db import models


class Worker(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=150, blank=True, default='')
    first_name = models.CharField(max_length=150, blank=True, default='')
    last_name = models.CharField(max_length=150, blank=True, default='')
    language = models.CharField(max_length=2, default='uz', blank=True, null=True)

    class Meta:
        verbose_name = 'Worker'
        verbose_name_plural = 'Workers'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        name = f"{self.first_name} {self.last_name}".strip() or f"User {self.telegram_id}"
        uname = f"(@{self.username})" if self.username else ''
        return f"{name} {uname}".strip()


class CheckIn(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='checkins')
    check_in_time = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='checkin_videos/')
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_name = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        verbose_name = 'Check-In'
        verbose_name_plural = 'Check-Ins'
        ordering = ['-check_in_time']

    def __str__(self):
        loc = self.location_name or f"({self.latitude}, {self.longitude})"
        return f"{self.worker}: {self.check_in_time:%Y-%m-%d %H:%M} at {loc}"
