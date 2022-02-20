"""
`busio` - Bus protocol support like I2C and SPI
=================================================

See `CircuitPython:busio` in CircuitPython for more details.

* Author(s): cefn
"""

try:
    import threading
except ImportError:
    threading = None

import my_adafruit_platformdetect_constants_chips as ap_chip
import my_adafruit_platformdetect


detector = my_adafruit_platformdetect.Detector()


class ContextManaged:
    """An object that automatically deinitializes hardware with a context manager."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.deinit()

    # pylint: disable=no-self-use
    def deinit(self):
        """Free any hardware used by the object."""
        return

    # pylint: enable=no-self-use


class Lockable(ContextManaged):
    """An object that must be locked to prevent collisions on a microcontroller resource."""

    _locked = False

    def try_lock(self):
        """Attempt to grab the lock. Return True on success, False if the lock is already taken."""
        if self._locked:
            return False
        self._locked = True
        return True

    def unlock(self):
        """Release the lock so others may use the resource."""
        if self._locked:
            self._locked = False
        else:
            raise ValueError("Not locked")


class SPI(Lockable):
    """
    Busio SPI Class for CircuitPython Compatibility. Used
    for both MicroPython and Linux.
    """

    def __init__(self, clock, MOSI=None, MISO=None):
        self.deinit()
        if detector.board.ftdi_ft232h:
            raise NotImplementedError("detector.board.ftdi_ft232h")
            from adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.ftdi_mpsse.ft232h.pin import (
                SCK,
                MOSI,
                MISO,
            )

            self._spi = _SPI()
            self._pins = (SCK, MOSI, MISO)
            return
        if detector.board.binho_nova:
            raise NotImplementedError("detector.board.binho_nova")
            from adafruit_blinka.microcontroller.nova.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.nova.pin import SCK, MOSI, MISO

            self._spi = _SPI(clock)
            self._pins = (SCK, MOSI, MISO)
            return
        if detector.board.greatfet_one:
            raise NotImplementedError("detector.board.greatfet_one")
            from adafruit_blinka.microcontroller.nxp_lpc4330.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.nxp_lpc4330.pin import SCK, MOSI, MISO

            self._spi = _SPI()
            self._pins = (SCK, MOSI, MISO)
            return
        if detector.board.pico_u2if:
            raise NotImplementedError("detector.board.pico_u2if")
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import SPI_Pico as _SPI

            self._spi = _SPI(clock)  # this is really all that's needed
            self._pins = (clock, clock, clock)  # will determine MOSI/MISO from clock
            return
        if detector.board.feather_u2if:
            raise NotImplementedError("detector.board.feather_u2if")
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import (
                SPI_Feather as _SPI,
            )

            self._spi = _SPI(clock)  # this is really all that's needed
            self._pins = (clock, clock, clock)  # will determine MOSI/MISO from clock
            return
        if detector.board.itsybitsy_u2if:
            raise NotImplementedError("detector.board.itsybitsy_u2if")
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import (
                SPI_ItsyBitsy as _SPI,
            )

            self._spi = _SPI(clock)  # this is really all that's needed
            self._pins = (clock, clock, clock)  # will determine MOSI/MISO from clock
            return
        if detector.board.macropad_u2if:
            raise NotImplementedError("detector.board.macropad_u2if")
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import (
                SPI_MacroPad as _SPI,
            )

            self._spi = _SPI(clock)  # this is really all that's needed
            self._pins = (clock, clock, clock)  # will determine MOSI/MISO from clock
            return
        if detector.board.qtpy_u2if:
            raise NotImplementedError("detector.board.qtpy_u2if")
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import SPI_QTPY as _SPI

            self._spi = _SPI(clock)  # this is really all that's needed
            self._pins = (clock, clock, clock)  # will determine MOSI/MISO from clock
            return
        if detector.chip.id == ap_chip.RP2040:
            raise NotImplementedError("detector.chip.id == ap_chip.RP2040")
            from adafruit_blinka.microcontroller.rp2040.spi import SPI as _SPI

            self._spi = _SPI(clock, MOSI, MISO)  # Pins configured on instantiation
            self._pins = (clock, clock, clock)  # These don't matter, they're discarded
            return

        from my_adafruit_blinka_microcontroller_generic_micropython_spi import (
            SPI as _SPI,
        )
        # from my_board import Pin
        
        # SPI_MO = Pin(4)  # EINT4  (pin 19)
        # SPI_MI = Pin(3)  # EINT3  (pin 21)
        # SPI_CLK = Pin(6)  # EINT6  (pin 23)

        # # ordered as spiId, sckId, mosiId, misoId
        # spiPorts = ((0, SPI_CLK, SPI_MO, SPI_MI),)

        # for portId, portSck, portMosi, portMiso in spiPorts:
        #     if (
        #         (clock == portSck)
        #         and MOSI in (portMosi, None)  # Clock is required!
        #         and MISO in (portMiso, None)  # But can do with just output
        #     ):  # Or just input
        #         self._spi = _SPI(portId)
        #         self._pins = (portSck, portMosi, portMiso)
        #         break
        # else:
        #     raise ValueError(
        #         "No Hardware SPI on (SCLK, MOSI, MISO)={}\nValid SPI ports:{}".format(
        #             (clock, MOSI, MISO), spiPorts
        #         )
        #     )

    def configure(self, baudrate=100000, polarity=0, phase=0, bits=8):
        """Update the configuration"""
        if detector.board.any_nanopi and detector.chip.id == ap_chip.SUN8I:
            raise NotImplementedError("")
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif detector.board.ftdi_ft232h:
            raise NotImplementedError("")
            from adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.spi import (
                SPI as _SPI,
            )
        elif detector.board.ftdi_ft2232h:
            raise NotImplementedError("")
            from adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.spi import (
                SPI as _SPI,
            )
        elif detector.board.binho_nova:
            raise NotImplementedError("")
            from adafruit_blinka.microcontroller.nova.spi import SPI as _SPI
        elif detector.board.greatfet_one:
            raise NotImplementedError("")
            from adafruit_blinka.microcontroller.nxp_lpc4330.spi import SPI as _SPI
        elif detector.board.any_lubancat and detector.chip.id == ap_chip.IMX6ULL:
            raise NotImplementedError("")
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif detector.board.pico_u2if:
            raise NotImplementedError("")
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import SPI_Pico as _SPI
        elif detector.board.feather_u2if:
            raise NotImplementedError("")
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import (
                SPI_Feather as _SPI,
            )
        elif detector.board.itsybitsy_u2if:
            raise NotImplementedError("")
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import (
                SPI_ItsyBitsy as _SPI,
            )
        elif detector.board.macropad_u2if:
            raise NotImplementedError("")
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import (
                SPI_MacroPad as _SPI,
            )
        elif detector.board.qtpy_u2if:
            raise NotImplementedError("")
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import SPI_QTPY as _SPI
        elif detector.chip.id == ap_chip.RP2040:
            raise NotImplementedError("")
            from adafruit_blinka.microcontroller.rp2040.spi import SPI as _SPI
        elif detector.board.any_embedded_linux:
            raise NotImplementedError("")
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        else:
            from my_adafruit_blinka_microcontroller_generic_micropython_spi import (
                SPI as _SPI,
            )

        if self._locked:
            # TODO check if #init ignores MOSI=None rather than unsetting, to save _pinIds attribute
            # self._spi.init(
            #     baudrate=baudrate,
            #     polarity=polarity,
            #     phase=phase,
            #     bits=bits,
            #     firstbit=_SPI.MSB,
            # )
            print("self._spi.init")
        else:
            raise RuntimeError("First call try_lock()")

    def deinit(self):
        """Deinitialization"""
        self._spi = None
        self._pinIds = None

    @property
    def frequency(self):
        """Return the baud rate if implemented"""
        try:
            return self._spi.frequency
        except AttributeError as error:
            raise NotImplementedError(
                "Frequency attribute not implemented for this platform"
            ) from error

    def write(self, buf, start=0, end=None):
        """Write to the SPI device"""
        return self._spi.write(buf, start, end)

    def readinto(self, buf, start=0, end=None, write_value=0):
        """Read from the SPI device into a buffer"""
        return self._spi.readinto(buf, start, end, write_value=write_value)

    def write_readinto(
        self, buffer_out, buffer_in, out_start=0, out_end=None, in_start=0, in_end=None
    ):
        """Write to the SPI device and read from the SPI device into a buffer"""
        return self._spi.write_readinto(
            buffer_out, buffer_in, out_start, out_end, in_start, in_end
        )
        