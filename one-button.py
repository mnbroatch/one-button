import RPi.GPIO as GPIO
import math
import time
import threading

#GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(16, GPIO.IN)

def turn_light_on ():
    GPIO.output(18, GPIO.HIGH)
    
def turn_light_off ():
    GPIO.output(18, GPIO.LOW)

def toggle_light ():
    if GPIO.input(18): 
        GPIO.output(18, GPIO.LOW)
    else:
        GPIO.output(18, GPIO.HIGH)

def is_light_on ():
    return GPIO.input(18)

def is_button_pressed ():
    return GPIO.input(16)

current_level = 1

currently_interruptable_sequences = []



def cancel_animation_on_press (currently_interruptable_sequences):
    while not is_button_pressed():
        time.sleep(.001)
    for sequence in currently_interruptable_sequences:
        sequence.stop()

th_button = threading.Thread(target=cancel_animation_on_press, args=[currently_interruptable_sequences])
th_button.daemon = True 
th_button.start()


def make_blink_animation_curve (animation_duration, start_blink_duration, end_blink_duration):
    if start_blink_duration < end_blink_duration:
        x = animation_duration
        y = end_blink_duration
        h = 0
        k = start_blink_duration
    else: 
        x = 0
        y = start_blink_duration
        h = animation_duration
        k = end_blink_duration

    a = (y - k) / (x - h) ** 2
    return lambda time: a * (time - h) ** 2 + k


class Step:
    def __init__ (self, action, duration):
        self.action = action
        self.duration = duration

class StepSequence:
    active_timer = None

    def __init__ (self, step_list = []):
        self.step_list = step_list
        self.timers = []
        self.done = False

    def run (self, index = 0):
        step = self.step_list[index]
        step.action()

        if index != len(self.step_list) - 1:
            timer = threading.Timer(step.duration, lambda: self.run(index + 1))
            timer.daemon = True
            timer.start()
            active_timer = timer
        else:
            self.done = True

        while not self.done:
            pass
            time.sleep(.01)

    def stop (self):
        if self.active_timer:
            self.active_timer.cancel()

    def __add__ (self, other):
        self.step_list += other.step_list
        return self


def make_blink_sequence (duration):
    return StepSequence([
        Step(turn_light_on, duration),
        Step(turn_light_off, duration)
    ])


def make_pause_sequence (duration):
    return StepSequence([
        Step(lambda: None, duration)
    ])


def make_steady_blink_sequence (number_of_blinks, blink_duration):
    sequence = StepSequence()
    for _ in range(number_of_blinks):
        sequence += make_blink_sequence(blink_duration)
        sequence += make_pause_sequence(blink_duration)
    return sequence 

def make_blink_curve_sequence (sequence_duration, curve):
    sequence_duration_so_far = 0
    sequence = StepSequence()
    while sequence_duration_so_far < sequence_duration:
        current_step_duration = curve(sequence_duration_so_far)
        sequence += make_blink_sequence(curve(sequence_duration_so_far))
        sequence_duration_so_far += current_step_duration
    return sequence 

test_animation_curve = make_blink_animation_curve(1, .05, .165)

print("1")
make_blink_sequence(.5).run()
print("2")

while True:
    pass
