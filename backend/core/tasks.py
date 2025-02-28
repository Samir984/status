# tasks.py
import dramatiq
import httpx
from django.utils import timezone
from dramatiq_crontab import cron  # type: ignore

from .models import Log
from .models import Service
from .utils import send_discord_alert


@cron("* * * * *")
@dramatiq.actor  # type: ignore
def check_service_status():
    now = timezone.now()
    print(f"Current time: {now}")
    services = Service.objects.filter(is_paused=False)

    if not services:
        return
    temp_log: list[Log] = []

    for service in services:
        is_up = False
        status_code = 500  #
        try:
            response = httpx.get(service.url, timeout=5)
            if response.is_success:  # 200-299
                is_up = True
                status_code = response.status_code
            elif response.status_code in range(400, 600):
                is_up = False
                status_code = response.status_code

        except (httpx.RequestError, httpx.TimeoutException):
            is_up = False

        temp_log.append(
            Log(service=service, is_up=is_up, status_code=status_code)
        )

    if temp_log:
        # create logs
        Log.objects.bulk_create(temp_log)

        # send discord notification
    down_logs = [log for log in temp_log if not log.is_up]
    if down_logs:
        send_discord_alert(down_logs)
