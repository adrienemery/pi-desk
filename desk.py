import time

# gpiocrust imports
try:
    import RPi.GPIO as GPIO
except ImportError:
    ENV = 'local'
else:
    ENV = 'pi'

LOCAL = 'local'
PI = 'pi'

if ENV == PI:
    GPIO.setmode(GPIO.BCM)
    # change these as desired - they're the pins connected from the
    # SPI port on the ADC to the Cobbler
    SPICLK = 18
    SPIMISO = 23
    SPIMOSI = 24
    SPICS = 25

    # set up the SPI interface pins
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)


# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

def cleanup():
    if ENV == PI:
        GPIO.cleanup()

class Desk(object):

    PWM_PIN = 13
    UP_PIN = 19
    DOWN_PIN = 26
    UP = 'up'
    DOWN = 'down'
    STOPPED = 'stopped'
    MICROS_TO_INCH = 1/147.0
    SONAR_ADC_CH = 0
    SONAR_ORIENTATION = UP

    def __init__(self):
        DEBUG = 1
        self.height = None
        self.last_height = None
        self.direction = None
        self.threshold = 3
        self.sensor = None
        self.start_time = None
        self.stop_time = None
        self.update_height()
        if ENV == PI:
            GPIO.setup(self.UP_PIN, GPIO.OUT)
            GPIO.setup(self.DOWN_PIN, GPIO.OUT)

    def __del__(self):
        if ENV == PI:
            GPIO.cleanup()

    def move(self, setpoint):
        if self.SONAR_ORIENTATION == self.UP:
            if setpoint < self.height:
                self.move_up(setpoint)
            elif setpoint > self.height:
                self.move_down(setpoint)

        elif self.SONAR_ORIENTATION == self.DOWN:
            if setpoint > self.height:
                self.move_up(setpoint)
            elif setpoint > self.height:
                self.move_down(setpint)

    def move_up(self, setpoint=None):
        """Move the desk up.
        If a setpoint is provided we move up to that setpoint otherwise keep moving
        until a stop command is recieved.

        Setting the output pin to LOW or False triggers motion in a given direction.
        """
        print 'Moving up'
        if ENV == PI:
            GPIO.output(self.DOWN_PIN, True)
            GPIO.output(self.UP_PIN, False)

	    if setpoint is None: return

        if self.SONAR_ORIENTATION == self.DOWN:
            if setpoint > self.height:
                while self.height < setpoint:
                    self.update_height()
                self.stop()
            else:
                self.stop()
                print 'Cannot move up to a setpoint below current position'

        elif self.SONAR_ORIENTATION == self.UP:
            if setpoint < self.height:
                while self.height > setpoint:
                    self.update_height()
                self.stop()
            else:
                self.stop()
                print 'Cannot move up to a setpoint below current position'

    def move_down(self, setpoint=None):
        """Move the desk down.
        If a setpoint is provided we move down to that setpoint otherwise keep moving
        until a stop command is recieved.

        Setting the output pin to LOW or False triggers motion in a given direction.
        """
        print 'Moving down'
        if ENV == PI:
            GPIO.output(self.UP_PIN, True)
            GPIO.output(self.DOWN_PIN, False)

        if setpoint is None: return

        if self.SONAR_ORIENTATION == self.DOWN:
            if setpoint < self.height:
                while self.height > setpoint:
                    self.update_height()
                self.stop()
            else:
                self.stop()
                print 'Cannot move down to a setpoint above current position'
        elif self.SONAR_ORIENTATION == self.UP:
            if setpoint > self.height:
                while self.height < setpoint:
                    self.update_height()
                self.stop()
            else:
                self.stop()
                print 'Cannot move down to a setpoint above current position'


    def stop(self):
        """Stop moving.
        """
        print 'Stopping'
        if ENV == PI:
            # set both output pins to HIGH
            GPIO.output(self.UP_PIN, True)
            GPIO.output(self.DOWN_PIN, True)

    def update_height(self):
        if ENV == PI:
            adc_val = readadc(self.SONAR_ADC_CH,  SPICLK, SPIMOSI, SPIMISO, SPICS)
            voltage = (adc_val / 1024.0) * 3.3
            volts_per_inch = 3.3 / 512.0
            self.height = voltage / volts_per_inch

        else:
            self.height = 0
