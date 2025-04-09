import st7735 as TFT
import RPi.GPIO as GPIO
import spi as SPI
from PIL import Image, ImageDraw, ImageFont

WIDTH = 128
HEIGHT = 160
SPEED_HZ = 4000000

DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0


# Create TFT LCD display class.
disp = TFT.ST7735(
    DC,
    rst=RST,
    spi=SPI.SpiDev(
        SPI_PORT,
        SPI_DEVICE,
        max_speed_hz=SPEED_HZ))

# Initialize display.
disp.begin()



fontSize = 10
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontSize)

def updateLCD(disp, text):
    # Load an image.
    # print('Loading image...')
    # image = Image.open('cat.jpg')

    # # Resize the image and rotate it so matches the display.
    # image = image.rotate(90).resize((WIDTH, HEIGHT))
    image = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    for i, t in enumerate(text):
        if t != '':
            w = draw.textlength(t, font=font)
            h = fontSize
            draw.text((0, i*(h)), t, font=font, fill=(255, 255, 255))

    # Draw the image on the display hardware.
    # print('Drawing image')
    image = image.rotate(90).resize((WIDTH, HEIGHT))
    disp.display(image)
