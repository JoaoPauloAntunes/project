class Pin:
    """A basic Pin class for use with FTDI MPSSEs."""

    IN = 0
    OUT = 1
    LOW = 0
    HIGH = 1
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2

    mpsse_gpio = None

    def __init__(self, pin_id=None):
        self.id = pin_id


C0 = Pin(8)
C1 = Pin(9)