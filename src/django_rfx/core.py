import RFXtrx
from socket import error as socket_error
from os.path import exists
import logging
import time

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger("RFXtrx")

core = None

rfxcom_device = None


class RFXhandler:
    core = None
    rfxcom_device = None
    modes_list = []

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(RFXhandler, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        log.debug("Init")
        self.modes_list = ["ac", "fineoffset"]

    def set_state(self, id: str, packet_type: str, state: bool) -> bool:
        log.debug(
            "Set State - ID: {} PacketType: {} State: {}".format(id, packet_type, state)
        )

        if self.core is None:
            log.error("Unable to set state, not connected")
            return False

        pkt = RFXtrx.lowlevel.PACKET_TYPES[int(packet_type, 0)]()
        pkt.parse_id(0x00, id.lower())
        dev = RFXtrx.LightingDevice(pkt)
        try:
            if state:
                dev.send_on(self.core.transport)
            else:
                dev.send_off(self.core.transport)

            return True
        except BrokenPipeError:
            self.reconnec()
            self.set_state(id, packet_type, state)

    def set_level(self, id: str, packet_type: str, level: int) -> bool:
        log.debug(
            "Set Level - ID: {} PacketType: {} Level: {}".format(id, packet_type, level)
        )

        if self.core is None:
            log.error("Unable to set brightness, not connected")
            return False

        pkt = RFXtrx.lowlevel.PACKET_TYPES[int(packet_type, 0)]()
        pkt.parse_id(0x00, id.lower())
        dev = RFXtrx.LightingDevice(pkt)
        try:
            dev.send_dim(self.core.transport, level)
        except BrokenPipeError:
            self.reconnec()
            self.set_level(id, packet_type, level)

    def rfx_callback(self, event):
        log.debug("Received {}".format(event))
        return
        if isinstance(event, RFXtrx.SensorEvent):
            log.debug("Received sensor event: {}".format(event))
            packet_type = event.device.packettype
            create_or_update(packet_type, event)
        elif isinstance(event, RFXtrx.ControlEvent):
            log.debug("Received control event {} - {}".format(event, event.device))
        else:
            log.debug("Received unknown event {}".format(event))

    def connect(self, device=None):
        # from .handlers import rfx_callback
        self.rfxcom_device = device if device is not None else self.rfxcom_device
        d = self.rfxcom_device.split(":")
        if len(d) == 2:
            self.rfxcom_device = (d[0], int(d[1]))
        else:
            self.rfxcom_device = d[0]

        if isinstance(self.rfxcom_device, tuple):
            proto = RFXtrx.PyNetworkTransport
        else:
            if not exists(self.rfxcom_device):
                log.error("Serial device {} not found".format(self.rfxcom_device))
                return
            else:
                proto = RFXtrx.PySerialTransport

        log.debug(
            "Opening rfxcom on {} with protocol {}".format(self.rfxcom_device, proto)
        )

        try:
            self.core = RFXtrx.Core(
                self.rfxcom_device,
                self.rfx_callback,
                modes=self.modes_list,
                transport_protocol=proto,
            )
            log.info("RFX connected")
        except AttributeError:
            time.sleep(1)
            self.connect()
        except socket_error:
            print("Shite")
        # except Exception as e:
        #    print(type(e).__name__)

    def reconnec(self):
        if self.core is None:
            log.debug("Reconnect - Not connected")
        else:
            log.debug("Closing connection")
            self.core.close_connection()
        log.debug("Reconnecting")
        self.connect()

    def disconnect(self):
        if self.core is not None:
            log.debug("Closing connection")
            self.core.close_connection()
            log.debug("Setting core to None")
            self.core = None
        else:
            log.debug("Disconnect called, but not connected")


_instance = RFXhandler()

connect = _instance.connect
disconnect = _instance.disconnect
set_state = _instance.set_state
set_level = _instance.set_level


def reconnect(device=None):
    global _instance
    device = _instance.rfxcom_device if device is None else device
    _instance.disconnect()
    _instance.connect(device)
