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


CE0 = Pin("SPI0_CS0")  # P9_17
MOSI = Pin("SPI0_D1")  # P9_18
MISO = Pin("SPI0_D0")  # P9_21
SCLK = Pin("SPI0_SCLK")  # P9_22


def SPI():
    """The singleton SPI interface"""
    import my_busio

    return my_busio.SPI(SCLK, MOSI, MISO)
        

C0 = Pin(8)
C1 = Pin(9)