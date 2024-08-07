##led_strip_animations.py
#to control the led strip via push button

#imports necessary for the button
from button import Button

#imports necessary for the led strip
from rpi_ws281x import PixelStrip, Color
import argparse
import time

class LEDAnimation(PixelStrip, Color):
    def __init__(self, led_count, led_pin, led_freq_hz, led_dma, led_brightness, led_invert, led_channel):
        super().__init__(led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, led_channel)
        self.begin()

    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.setPixelColor(i, color)
            self.show()
            time.sleep(wait_ms / 1000.0)

    def theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.numPixels(), 3):
                    self.setPixelColor(i + q, color)
                self.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.numPixels(), 3):
                    self.setPixelColor(i + q, 0)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color.RGBW(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color.RGBW(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color.RGBW(0, pos * 3, 255 - pos * 3)

    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.setPixelColor(i, self.wheel((i + j) & 255))
            self.show()
            time.sleep(wait_ms / 1000.0)

    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * iterations):
            for i in range(self.numPixels()):
                self.setPixelColor(i, self.wheel((int(i * 256 / self.numPixels()) + j) & 255))
            self.show()
            time.sleep(wait_ms / 1000.0)

    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.numPixels(), 3):
                    self.setPixelColor(i + q, self.wheel((i + j) % 255))
                self.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.numPixels(), 3):
                    self.setPixelColor(i + q, 0)


if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # LED strip configuration:
    LED_COUNT = 69        # Number of LED pixels.
    LED_PIN = 18          # GPIO pin connected to the strip
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10          # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    
    strip = LEDAnimation(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    
    
    # Animation
    animation = 0

    def change_animation():
        global animation
        animation = (animation + 1) % 6 # to keep animation between 0-5

    # Button configuration
    BUTTON_PIN = 17  # GPIO pin connected to the button
    button = Button(BUTTON_PIN, callback=change_animation)


    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            if animation == 0:
                strip.colorWipe(Color.RGBW(255, 0, 0))  # Red wipe
            elif animation == 1:
                strip.colorWipe(Color.RGBW(0, 255, 0))  # Green wipe
            elif animation == 2:
                strip.colorWipe(Color.RGBW(0, 0, 255))  # Blue wipe
            elif animation == 3:
                strip.theaterChase(Color.RGBW(127, 127, 127))  # White theater chase
            elif animation == 4:
                strip.rainbow()
            elif animation == 5:
                strip.rainbowCycle()

    except KeyboardInterrupt:
        if args.clear:
            strip.colorWipe(Color.RGBW(0, 0, 0), 10)
        button.cleanup()