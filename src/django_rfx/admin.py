from typing import Any, Dict, Optional
from django.contrib import admin
from django.http.request import HttpRequest
from django.template.response import TemplateResponse

# Register your models here.

from .models import PacketType, Protocol
from .core import set_modes, reconnect


@admin.register(Protocol)
class ProtocolAdmin(admin.ModelAdmin):
    ordering = ["description"]
    list_display = ["description", "enabled"]
    list_editable = ["enabled"]

    # def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
    #    print(obj)
    #    return super().save_model(request, obj, form, change)

    def changelist_view(
        self, request: HttpRequest, extra_context=None
    ) -> TemplateResponse:
        retVal = super().changelist_view(request, extra_context)
        if "_save" in request.POST:
            set_modes()
            reconnect()

        return retVal
