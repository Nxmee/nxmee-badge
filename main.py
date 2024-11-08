import badger2040
from badger2040 import HEIGHT, WIDTH

from code_gen import make_code
DATA_PATH = "data.txt"
QR_SIZE = 100
QR_X = WIDTH-QR_SIZE 
QR_Y = 0
QR_PADDING = 4
BLACK = 0
WHITE = 15
GREY = 12

display = badger2040.Badger2040()



def _draw_code(matrix,x_offset,y_offset):
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            display.set_pen(BLACK if matrix[x][y] else WHITE)
            display.pixel(x+x_offset,y+y_offset)
        
def code(data, size, x, y):
    code = make_code(data, size)
    _draw_code(code, x, y)

def centered_multiline_text(text, font, font_height, x, y, line_gap=0, scale=1):
    spacing=1
    
    display.set_font(font)
    display.set_pen(BLACK)
    current_y = y
    for line in text:
        line_width = display.measure_text(line,scale,spacing)
        text_x = x - (line_width//2)
        display.text(line, text_x, current_y, scale=scale, spacing=spacing)
        current_y += font_height*scale + line_gap
        
def up_arrow(root_x, root_y, width, height):
    a_x1 = root_x
    a_y1 = root_y
    a_x2 = root_x + width
    a_y2 = a_y1
    a_x3 = root_x + (width//2)
    a_y3 = root_y - height

    display.set_pen(BLACK)
    display.triangle(a_x1, a_y1,
                     a_x2, a_y2,
                     a_x3, a_y3)



display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_NORMAL)
display.set_thickness(2)

data = open(DATA_PATH, "r")
code_data = data.readline()
code_date = data.readline()

display.clear()

display.set_pen(WHITE)
display.rectangle(0,0,WIDTH,HEIGHT)

#QR Code Section
code(code_data,QR_SIZE,QR_X,QR_Y)

centered_multiline_text(["Fun Thing", "Of The Day", code_date],
                        "bitmap8", 8,
                        QR_X + (QR_SIZE//2),
                        QR_SIZE + QR_Y,
                        2)

a_width = 12
a_height = 12
a_offset = 5
a_root_x = WIDTH - a_width - a_offset
a_root_y = QR_SIZE + a_height

up_arrow(a_root_x, a_root_y, a_width, a_height)

#Name Section
display.set_pen(GREY)
display.rectangle(0, 0, WIDTH-QR_SIZE-QR_PADDING, HEIGHT)

TEXT_WIDTH = WIDTH-QR_SIZE-QR_PADDING

centered_multiline_text(["CHRIS", "HART"],
                        "bitmap8", 8,
                        TEXT_WIDTH//2,
                        0,
                        scale=8)

display.update()
