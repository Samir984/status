from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)
    url = models.URLField()
    token = models.CharField(max_length=255, null=True, blank=True)
    # True if the service is paused for monitoring
    is_paused = models.BooleanField(default=False)
    data_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Log(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="log")
    is_up = models.BooleanField(default=False)
    last_checked = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return (
            f"{self.service.name} - {'Up' if self.is_up else 'Down'} at"
            f" {self.last_checked}"
        )


class Notification(models.Model):
    service = models.OneToOneField(
        Service, on_delete=models.CASCADE, related_name="notification"
    )
    webhook_url = models.TextField(default="")
    # True if the notification is paused
    is_paused = models.BooleanField(default=False)

    def __str__(self):
        return f"ServiceNotification #{self.pk}"
