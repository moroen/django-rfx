# Generated by Django 4.1.7 on 2023-04-02 22:17

from django.db import migrations
from django_rfx.models import PacketType, Protocol
from django_rfx.packet_types import PacketTypes

def create_defaults(app, editor):
    for key, value in PacketTypes.items():
        PacketType(id=key, description=value).save()

    Protocol(description="ac").save()
    Protocol(description="arc").save()
    Protocol(description="fineoffset").save()


# def create_defaults(app, editor):
#     PacketType(id="0x01", description="Status").save()
#     PacketType(id="0x03", description="Undecoded").save()
#     PacketType(id="0x10", description="Lighting1").save()
#     PacketType(id="0x11", description="Lighting2").save()
#     PacketType(id="0x12", description="Lighting3").save()
#     PacketType(id="0x13", description="Lighting4").save()
#     PacketType(id="0x14", description="Lighting5").save()
#     PacketType(id="0x15", description="Lighting6").save()
#     PacketType(id="0x16", description="Chime").save()
#     PacketType(id="0x19", description="RollerTrol").save()
#     PacketType(id="0x1A", description="Rfy").save()
#     PacketType(id="0x1E", description="Funkbus").save()
#     PacketType(id="0x20", description="Security1").save()
#     PacketType(id="0x4E", description="Bbq").save()
#     PacketType(id="0x4F", description="Temperature+Rain").save()
#     PacketType(id="0x50", description="Temp").save()
#     PacketType(id="0x51", description="Humidity").save()
#     PacketType(id="0x52", description="Temperature+Humidity").save()
#     PacketType(id="0x53", description="Barometer").save()
#     PacketType(id="0x54", description="Temperature+Humidity+Barometer").save()
#     PacketType(id="0x55", description="Rain").save()
#     PacketType(id="0x56", description="Wind").save()
#     PacketType(id="0x57", description="UV").save()
#     PacketType(id="0x59", description="Energy1").save()
#     PacketType(id="0x5A", description="Energy").save()
#     PacketType(id="0x5B", description="Energy4").save()
#     PacketType(id="0x5C", description="Energy5").save()
#     PacketType(id="0x59", description="Energy1").save()
#     PacketType(id="0x60", description="Cartelectronic").save()
#     PacketType(id="0x71", description="RfxMeter").save()

#     Protocol(description="ac").save()
#     Protocol(description="arc").save()
#     Protocol(description="fineoffset").save()


class Migration(migrations.Migration):
    dependencies = [
        ("django_rfx", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_defaults)]
