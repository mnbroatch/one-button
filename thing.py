import RPi.GPIO as GPIO
import thread
import time
import math

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(16, GPIO.IN)

current_level = 1

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


def blink_rate_change_animation (animation_duration, start_blink_duration, end_blink_duration):

    curve = make_blink_animation_curve(animation_duration, start_blink_duration, end_blink_duration)
    now = time.time()
    current_action_duration = curve(0)

    current_action_start_time = now
    current_action_end_time = current_action_start_time + current_action_duration


    animation_start_time = time.time()
    animation_end_time = animation_start_time + animation_duration


    while now < animation_end_time:
        if is_button_pressed():
            button_has_been_pushed = True
            break

        now = time.time()

        if now > current_action_end_time:
            current_action_duration = curve(now - animation_start_time)
            current_action_start_time = now
            current_action_end_time = current_action_start_time + current_action_duration
            toggle_light()

    turn_light_off()


def steady_blink_animation (number_of_blinks, blink_duration):

    now = time.time()
    current_action_end_time = now + blink_duration

    actions_so_far = 0
    while actions_so_far < number_of_blinks * 2:
        if is_button_pressed():
            button_has_been_pushed = True
            break

        now = time.time()
        if now > current_action_end_time:
            current_action_end_time = now + blink_duration
            actions_so_far = actions_so_far + 1
            toggle_light()

    turn_light_off()


def pause (animation_duration):

    now = time.time()
    animation_end_time = now + animation_duration

    while now < animation_end_time:
        if is_button_pressed():
            button_has_been_pushed = True
            break

        now = time.time()


def demo ():
    button_has_been_pushed = False
    while not button_has_been_pushed:
        blink_rate_change_animation(1, .05, .165)
        blink_rate_change_animation(1, .165, .05)
        pause(.3)
        steady_blink_animation(1, .3)
        pause(.6)

def level_1_question ():
    button_has_been_pushed = False
    while not button_has_been_pushed:
        pause(.6)
        steady_blink_animation(3, .3)
        pause(.6)

def level_1_answer ():
    button_presses = 0
    time_since_last_action = 0
    last_button_valence = False
    while time_since_last_action < 2 and not is_button_pressed():
        current_button_valence = is_button_pressed()
        if last_button_valence and not current_button_valence
            button_presses += 1
    return button_presses    

def level_1 ():
    level_1_question()
    while level_1_answer() != 3:
        level_1_question()





# Main
demo()
level_1()

print("level 3")

