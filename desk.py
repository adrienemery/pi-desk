import time

# gpiocrust imports
from gpiocrust import Header, OutputPin, InputPin


class Desk(object):

    PWM_PIN = 33
    UP_PIN = 35
    DOWN_PIN = 37
    UP = 'up'
    DOWN = 'down'
    STOPPED = 'stopped'
    MICROS_TO_INCH = 1/147.0

    def __init__(self):
        self.height = None
        self.last_height = None
        self.direction = None
        self.threshold = 3
        self.header = Header()
        self.stop()
        self.sensor = None

    def setup_sonar_sensor(self):
        self.sensor = InputPin(self.PWM_PIN, bouncetime=20, value=0, callback=self.edge_handler)

    def move(self, setpoint):
        if setpoint > self.height:
            self.move_up()
        elif setpoint < self.height:
            self.move_down()

    def move_up(self, setpoint=None):
        """Move the desk up.
        If a setpoint is provided we move up to that setpoint otherwise keep moving
        until a stop command is recieved.

        Setting the output pin to LOW or False triggers motion in a given direction.
        """
        print 'Moving up'
        if setpoint is None:
            OutputPin(self.DOWN_PIN).value = True
            OutputPin(self.UP_PIN).value = False
        elif setpoint > self.height:
            while abs(self.height - setpoint) < self.threshold:
                self.update_height()
            self.stop()
        else:
            raise RuntimeWarning('Cannot move up to a setpoint below current position')


    def move_down(self, setpoint=None):
        """Move the desk down.
        If a setpoint is provided we move down to that setpoint otherwise keep moving
        until a stop command is recieved.

        Setting the output pin to LOW or False triggers motion in a given direction.
        """
        print 'Moving down'
        if setpoint is None:
            OutputPin(self.UP_PIN).value = True
            OutputPin(self.DOWN_PIN).value = False

        elif setpoint < self.height:
            while abs(self.height - setpoint) < self.threshold:
                self.update_height()
            self.stop()
        else:
            raise RuntimeWarning('Cannot move down to a setpoint above current position')

    def stop(self):
        """Stop moving.
        """
        print 'Stopping'
        # set both output pins to HIGH
        OutputPin(self.UP_PIN).value = True
        OutputPin(self.DOWN_PIN).value = True

    def edge_handler(self, value):
        if self.start_time is None:
            self.start_time = time.clock()
            return
        elif self.stop_time is None:
            self.stop_time = time.clock()
            return
        else:
            total_time_us = (self.stop_time - self.start_time) / 10**6
            self.height = total_time_us * self.MICROS_TO_INCH
            # determine the direction of movement
            # we need to skip the first time around since last_height won't be set
            if self.last_height is not None:
                if self.last_height < self.height:
                    self.direction = self.UP
                elif self.last_height > self.height:
                    self.direcetion = self.DOWN
            # update last height
            self.last_height = self.height
            # reset timers
            self.stop_time = None
            self.start_time = None


if __name__ == '__main__':
    desk = Desk()
