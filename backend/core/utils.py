import logging
from typing import Any

import httpx
from django.db.models import F
from django.utils import timezone

from .models import Log

logger = logging.getLogger(__name__)


def send_discord_alert(down_logs: list[Log]):
    logs_id = [log.pk for log in down_logs]

    detail_logs = Log.objects.filter(id__in=logs_id).annotate(
        service_name=F("service__name"),
        notification_is_paused=F("service__notification__is_paused"),
        webhook_url=F("service__notification__webhook_url"),
    )

    for log in detail_logs:
        if log.notification_is_paused:  # type: ignore
            return

        service_name = log.service_name  # type: ignore
        emoji = "❌"
        embeds: dict[str, Any] = {
            "title": f"{emoji}  {service_name} is Down",
            "color": 16711680,
            "fields": [
                {"name": "Name", "value": service_name, "inline": True},
                {
                    "name": "Status code",
                    "value": log.status_code,
                    "inline": True,
                },
                {
                    "name": "Last Checked",
                    "value": timezone.localtime(log.last_checked).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "inline": False,
                },
            ],
            "footer": {"text": "Service Bot"},
            "timestamp": timezone.localtime(log.last_checked).isoformat(),
        }

        headers = {"Content-Type": "application/json"}
        payload: dict[str, Any] = {
            "username": "Health check hook",
            "embeds": [embeds],
        }

        try:
            httpx.post(
                log.webhook_url,  # type: ignore
                json=payload,
                headers=headers,
                timeout=10,
            )

        except Exception:
            logger.info("Error occure, while sending discord notification.")
            pass
