from django.apps import AppConfig
from django.dispatch import receiver
from django.conf import settings

from .core import connect, disconnect, reconnect
import logging
from os import environ

log = logging.getLogger("RFXtrx")


class DjangoRfxConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_rfx"

    def ready(self) -> None:
        if not (
            environ.get("RUN_MAIN")
            or environ.get("RFX2MQTT_SERVER_GATEWAY_INTERFACE") == "asgi"
        ):
            return

        config = getattr(settings, "RFX_CONFIG", None)
        if config is None:
            log.debug("No settings specified")
        else:
            use_constance = (
                config["USE_CONSTANCE"] if "USE_CONSTANCE" in config else False
            )
            # print(use_constance)
            if use_constance:
                log.debug("Using constance")
                from constance import config
                from constance.signals import config_updated

                @receiver(config_updated)
                def constance_updated(sender, key, old_value, new_value, **kwargs):
                    if old_value is None:
                        return

                    device = new_value if key == "RFX_DEVICE" else config.RFX_DEVICE

                    log.debug(
                        "Constance settings changed, reconnecting to {}}".format(device)
                    )

                    reconnect(host=host, port=port)

                connect(device=config.RFX_DEVICE)
            else:
                if "DEVICE" in config:
                    device = config["DEVICE"]
                else:
                    device = "/dev/ttyAMC0"
                    log.warn(
                        "Using settings from settings.py, but DEVICE not specified. Using default ({})".format(
                            device
                        )
                    )

                connect(device=device)

        return super().ready()
