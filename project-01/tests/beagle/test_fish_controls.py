# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Fish Controls Tests
--------------------------------------------------------------------------
License:   MIT License

Copyright 2025 - Jackson Lieb

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
--------------------------------------------------------------------------

Tests for fish motor controls on BeagleBone hardware. Verifies GPIO and
PWM functionality for mouth, tail, and head animations.

--------------------------------------------------------------------------
"""

# import Adafruit_BBIO.GPIO as GPIO
# import Adafruit_BBIO.PWM as PWM
# import time

# # Verify these match your physical wiring before running
# STBY = "P1_06"
# MOUTH_PWM = "P1_36"
# MOUTH_IN1 = "P1_30"
# MOUTH_IN2 = "P1_32"
# BODY_PWM = "P1_33"
# BODY_IN1 = "P1_26"
# BODY_IN2 = "P1_28"

# # Setup
# #GPIO.setup(STBY, GPIO.OUT)
# GPIO.setup(MOUTH_IN1, GPIO.OUT)
# GPIO.setup(MOUTH_IN2, GPIO.OUT)
# GPIO.setup(BODY_IN1, GPIO.OUT)
# GPIO.setup(BODY_IN2, GPIO.OUT)
# PWM.start(MOUTH_PWM, 0)
# PWM.start(BODY_PWM, 0)


# print("Waking up Billy...")
# #GPIO.output(STBY, GPIO.HIGH) # Enable Driver

# try:
#     print("Mouth Open!")
#     GPIO.output(MOUTH_IN1, GPIO.HIGH)
#     GPIO.output(MOUTH_IN2, GPIO.LOW)
#     PWM.set_duty_cycle(MOUTH_PWM, 100) # Full speed open
#     time.sleep(1)
    
#     print("Mouth Closed!")
#     PWM.set_duty_cycle(MOUTH_PWM, 0) # Release spring
#     time.sleep(1)
    
#     print("Look at Me!")
#     GPIO.output(BODY_IN1, GPIO.HIGH)
#     GPIO.output(BODY_IN2, GPIO.LOW)
#     PWM.set_duty_cycle(BODY_PWM, 100)
#     time.sleep(1)
    
#     print("Wag Tail!")
#     PWM.set_duty_cycle(BODY_PWM, 0)
#     GPIO.output(BODY_IN1, GPIO.LOW)
#     GPIO.output(BODY_IN2, GPIO.HIGH)
#     PWM.set_duty_cycle(BODY_PWM, 100) # Full speed open
#     time.sleep(1)
    
    

# except KeyboardInterrupt:
#     pass

# PWM.stop(MOUTH_PWM)
# PWM.stop(BODY_PWM)
# GPIO.cleanup()