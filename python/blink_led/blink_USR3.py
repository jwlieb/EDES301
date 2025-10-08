# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Blink USR3
--------------------------------------------------------------------------
License:   
Copyright 2025 - Jackson Lieb

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Simple program that will use the Adafruit BBIO library to blink the USR3 
LED at 5 Hz (i.e. 5 full on/off cycles per second)

End on keyboard interrupt

--------------------------------------------------------------------------
"""

import Adafruit_BBIO.GPIO as GPIO
import time

# Specify USR3 LED
led_pin = "USR3"

# Set up the pin as an output
GPIO.setup(led_pin, GPIO.OUT)

print("Blinking USR3 at 5Hz. Press Ctrl+C to stop.")

try:
    while True:
        # Turn the LED on
        GPIO.output(led_pin, GPIO.HIGH)
        # Wait for 0.1 seconds (half of the 5Hz cycle, which is 1/5 = 0.2s)
        time.sleep(0.1)

        # Turn the LED off
        GPIO.output(led_pin, GPIO.LOW)
        # Wait for another 0.1 seconds
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopping.")
    # Clean up GPIO settings
    GPIO.cleanup()