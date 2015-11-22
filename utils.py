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
        # self.update_height()  # add back in when there is a timeout

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

    def update_height(self):
        """Determine the height based on the time between input PWM pulses.

        There are two possible starting conditions:
            1 - the input pin is LOW
            2 - the input pin is HIGH

        Case 1:
            ___|---|___

            In this case we will read pwm_state of False and immediatly break out
            of the first while loop.

            The second while loop will run until the pwm_state reads True in
            which case the timer will start and we go into the third while loop.

            In the third while loop we wait until the pwm_state reads False again
            which breaks out of the loop and we can get the total time for one
            pulse.

        Case 2:
            ---|___|---|___

            In this case we will wait until the pwm_state goes to False and break
            out of the first while loop.

            The second while loop will run until the pwm_state reads True in
            which case the timer will start and we go into the third while loop.

            In the third while loop we wait until the pwm_state reads False again
            which breaks out of the loop and we can get the total time for one
            pulse.

        """
        pwm_state = True
        pwm_pin = InputPin(self.PWM_PIN)
        # wait until the pwm state goes low again
        while pwm_state != False:
            pwm_state = pwm_state = pwm_pin.value

        while pwm_state != True:
            pwm_state = pwm_pin.value
        # now te pwm state is HIGH so we wait until it goes LOW and record how
        # long it takes
        t0 = time.clock()
        while pwm_state != False:
            # keep polling the pwm state until it goes LOW
            pwm_state = pwm_pin.value
        t1 = time.clock()
        # get total time in microseconds
        total_time_us = (t1 - t0)/10**6
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
        # sleep for 50 ms
        time.sleep(0.05)
