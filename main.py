import ili9341
import my_board
import my_digitalio


cs_pin = my_digitalio.DigitalInOut(my_board.C0)
dc_pin = my_digitalio.DigitalInOut(my_board.C1)
print('works!')