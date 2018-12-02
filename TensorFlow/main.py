# This program demonstrates how to control a servo

# Import the relevant libraries
import RPi.GPIO as GPIO
#import picamera
import time
import os
 
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
 
# set GPIO Pins
ServoPin1 = 7                                        # GPIO pin for the servo1
ServoPin2 = 13
ServoPin3 = 15
LedPin = 11                                     # GPIO pin for the LED

# set GPIO direction (IN / OUT)
GPIO.setup(ServoPin1, GPIO.OUT)                      # Set ServoPin's mode to out
GPIO.setup(ServoPin2, GPIO.OUT)                      # Set ServoPin's mode to out
GPIO.setup(ServoPin3, GPIO.OUT)                      # Set ServoPin's mode to out

# Set GPIO direction (IN / OUT)
GPIO.setup(LedPin, GPIO.OUT)                    # Set LedPin's mode to output

# The servo is controlled using Pulse Width Modulation (PWM)
# The next few lines of code take care of the required setup for this functionality
# The details are not important; you should not modify this code
# --- Start of the PWM setup ---
    # Set PWM parameters
pwm_frequency = 50
duty_min = 2.5 * float(pwm_frequency) / 50.0
duty_max = 12.5 * float(pwm_frequency) / 50.0

    # Helper function to set the duty cycle
def set_duty_cycle(angle):
    return ((duty_max - duty_min) * float(angle) / 180.0 + duty_min)

    # Create a PWM instance
pwm_servo1 = GPIO.PWM(ServoPin1, pwm_frequency)
pwm_servo2 = GPIO.PWM(ServoPin2, pwm_frequency)
pwm_servo3 = GPIO.PWM(ServoPin3, pwm_frequency)

# --- End of the PWM setup ---
recycling = False;
compost = False;
trash = False;

i = 0

# Initialize the camera
camera = picamera.PiCamera()

# Main program 
if __name__ == '__main__':

    try:
        
        # This code repeats forever
        while True:

            GPIO.output(LedPin, GPIO.HIGH) # LED on
            
            camera.start_preview()
            time.sleep(5)
            camera.capture('/home/pi/ieee-qfpa18-team15/TensorFlow/images/waste%s.jpg' % i)
            camera.stop_preview()
            camera.close()
            
            index_of_category = os.system('python3 label_image.py --graph=~/tmp/output_graph.pb --labels=~/tmp/output_labels.txt --input_layer=Placeholder --output_layer=final_result --image=/images/waste%s.jpg' % i)

            i++

            recycling = index_of_category == 1
            compost = index_of_category == 0
            trash = index_of_category == 2

            if (recycling):
                angle = 0
                pwm_servo1.start(set_duty_cycle(angle))
                time.sleep(1)
                       
                angle = 90
                pwm_servo1.start(set_duty_cycle(angle))
                time.sleep(1)
                recycling = False
                pwm_servo1.stop()
            elif (compost): 
                # Move the servo
                angle = 0
                pwm_servo2.start(set_duty_cycle(angle))
                time.sleep(1)
                           
                angle = 90
                pwm_servo2.start(set_duty_cycle(angle))
                time.sleep(1)
                compost = False
                pwm_servo2.stop()
            elif (trash): 
                # Move the servo
                angle = 0
                pwm_servo3.start(set_duty_cycle(angle))
                time.sleep(1)
                           
                angle = 90
                pwm_servo3.start(set_duty_cycle(angle))
                time.sleep(1)
                trash = False
                pwm_servo3.stop()
            
            
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Program stopped by User")
        GPIO.output(LedPin, GPIO.LOW) # LED off
        GPIO.cleanup() # Release resource
