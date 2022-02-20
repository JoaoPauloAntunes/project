import ili9341
import my_board
import my_digitalio


cs_pin = my_digitalio.DigitalInOut(my_board.C0)
dc_pin = my_digitalio.DigitalInOut(my_board.C1)

disp = ili9341.ILI9341(my_board.SPI(), cs=cs_pin, dc=dc_pin, baudrate=64000000)


print('works!')