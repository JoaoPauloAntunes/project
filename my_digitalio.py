"""
`digitalio` - Digital input and output control (GPIO)
=====================================================

See `CircuitPython:digitalio` in CircuitPython for more details.

* Author(s): cefn
"""
import my_adafruit_platformdetect


detector = my_adafruit_platformdetect.Detector()
board_id = detector.board.id
chip_id = detector.chip.id


class Pin:
    """A basic Pin class for the NXP LPC4330 that
    acts as a wrapper for the GreatFET api.
    """

    # pin modes
    OUT = 1
    IN = 0
    ADC = 2
    DAC = 3

    # pin values
    LOW = 0
    HIGH = 1

    def __init__(self, pin_id=None):
        self.id = pin_id
        self._mode = None
        self._pin = None

    def init(self, mode=IN, pull=None):
        """Initialize the Pin"""
        if self.id is None:
            raise RuntimeError("Can not init a None type pin.")
        if pull is not None:
            raise NotImplementedError("Internal pullups and pulldowns not supported")
        if mode in (Pin.IN, Pin.OUT):
            # self._pin = my_gpio.get_pin(self.id)
            # self._pin.set_direction(mode)
            self._pin = None
        elif mode == Pin.ADC:
            raise NotImplemented("Pin.ADC")

            # ADC only available on these pins
            if self.id not in ADC_MAPPINGS:
                raise ValueError("Pin does not have ADC capabilities")
            self._pin = ADC(gf, self.id)
        elif mode == Pin.DAC:
            raise NotImplemented("Pin.DAC")

            # DAC only available on these pins
            if self.id != "J2_P5":
                raise ValueError("Pin does not have DAC capabilities")
            self._pin = gf.apis.dac
            self._pin.initialize()
        else:
            raise ValueError("Incorrect pin mode: {}".format(mode))
        self._mode = mode

    def value(self, val=None):
        """Set or return the Pin Value"""
        # Digital In / Out
        if self._mode in (Pin.IN, Pin.OUT):
            # digital read
            if val is None:
                return self._pin.get_state()
            # digital write
            if val in (Pin.LOW, Pin.HIGH):
                print({"val": val})
                # self._pin.set_state(val)
                return None
            # nope
            raise ValueError("Invalid value for pin.")
        # Analog In
        if self._mode == Pin.ADC:
            if val is None:
                # Read ADC here
                return self._pin.read_samples()[0]
            # read only
            raise AttributeError("'AnalogIn' object has no attribute 'value'")
        # Analog Out
        if self._mode == Pin.DAC:
            if val is None:
                # write only
                raise AttributeError("unreadable attribute")
            # Set DAC Here
            self._pin.set_value(int(val))
            return None
        raise RuntimeError(
            "No action for mode {} with value {}".format(self._mode, val)
        )

class Enum:
    """
    Object supporting CircuitPython-style of static symbols
    as seen with Direction.OUTPUT, Pull.UP
    """

    def __repr__(self):
        """
        Assumes instance will be found as attribute of own class.
        Returns dot-subscripted path to instance
        (assuming absolute import of containing package)
        """
        cls = type(self)
        for key in dir(cls):
            if getattr(cls, key) is self:
                return "{}.{}.{}".format(cls.__module__, cls.__qualname__, key)
        return repr(self)

    @classmethod
    def iteritems(cls):
        """
        Inspects attributes of the class for instances of the class
        and returns as key,value pairs mirroring dict#iteritems
        """
        for key in dir(cls):
            val = getattr(cls, key)
            if isinstance(cls, val):
                yield (key, val)


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


class DriveMode(Enum):
    """Drive Mode Enumeration"""

    PUSH_PULL = None
    OPEN_DRAIN = None


DriveMode.PUSH_PULL = DriveMode()
DriveMode.OPEN_DRAIN = DriveMode()


class Direction(Enum):
    """Direction Enumeration"""

    INPUT = None
    OUTPUT = None


Direction.INPUT = Direction()
Direction.OUTPUT = Direction()


class Pull(Enum):
    """PullUp/PullDown Enumeration"""

    UP = None
    DOWN = None
    # NONE=None


Pull.UP = Pull()
Pull.DOWN = Pull()

# Pull.NONE = Pull()


class DigitalInOut(ContextManaged):
    """DigitalInOut CircuitPython compatibility implementation"""

    _pin = None

    def __init__(self, pin):
        self._pin = Pin(pin.id)
        self.direction = Direction.INPUT

    def switch_to_output(self, value=False, drive_mode=DriveMode.PUSH_PULL):
        """Switch the Digital Pin Mode to Output"""
        self.direction = Direction.OUTPUT
        self.value = value
        self.drive_mode = drive_mode

    def switch_to_input(self, pull=None):
        """Switch the Digital Pin Mode to Input"""
        self.direction = Direction.INPUT
        self.pull = pull

    def deinit(self):
        """Deinitialize the Digital Pin"""
        del self._pin

    @property
    def direction(self):
        """Get or Set the Digital Pin Direction"""
        return self.__direction

    @direction.setter
    def direction(self, value):
        self.__direction = value
        if value is Direction.OUTPUT:
            self._pin.init(mode=Pin.OUT)
            self.value = False
            self.drive_mode = DriveMode.PUSH_PULL
        elif value is Direction.INPUT:
            self._pin.init(mode=Pin.IN)
            self.pull = None
        else:
            raise AttributeError("Not a Direction")

    @property
    def value(self):
        """The Digital Pin Value"""
        return self._pin.value() == 1

    @value.setter
    def value(self, val):
        if self.direction is Direction.OUTPUT:
            self._pin.value(1 if val else 0)
        else:
            raise AttributeError("Not an output")

    @property
    def pull(self):
        """The pin pull direction"""
        if self.direction is Direction.INPUT:
            return self.__pull
        raise AttributeError("Not an input")

    @pull.setter
    def pull(self, pul):
        if self.direction is Direction.INPUT:
            self.__pull = pul
            if pul is Pull.UP:
                self._pin.init(mode=Pin.IN, pull=Pin.PULL_UP)
            elif pul is Pull.DOWN:
                if hasattr(Pin, "PULL_DOWN"):
                    self._pin.init(mode=Pin.IN, pull=Pin.PULL_DOWN)
                else:
                    raise NotImplementedError(
                        "{} unsupported on {}".format(Pull.DOWN, board_id)
                    )
            elif pul is None:
                self._pin.init(mode=Pin.IN, pull=None)
            else:
                raise AttributeError("Not a Pull")
        else:
            raise AttributeError("Not an input")

    @property
    def drive_mode(self):
        """The Digital Pin Drive Mode"""
        if self.direction is Direction.OUTPUT:
            return self.__drive_mode  #
        raise AttributeError("Not an output")

    @drive_mode.setter
    def drive_mode(self, mod):
        self.__drive_mode = mod
        if mod is DriveMode.OPEN_DRAIN:
            self._pin.init(mode=Pin.OPEN_DRAIN)
        elif mod is DriveMode.PUSH_PULL:
            self._pin.init(mode=Pin.OUT)
