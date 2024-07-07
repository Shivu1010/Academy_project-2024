import os
import time
import picamera
import pytesseract
from gtts import gTTS
import RPi.GPIO as GPIO

# Set up GPIO
GPIO.setmode(GPIO.BCM)
button_pin = 2
GPIO.setwarnings(False)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up the camera
os.system('espeak "{Ok Ready to Capture}"')
camera = picamera.PiCamera()
camera.resolution = (1024, 768)

def capture_and_convert():
    # Capture an image
    camera.capture('image.jpg')

    # Convert the image to text using OCR
    text = pytesseract.image_to_string('image.jpg')

    print(text)

    # Check if text is detected
    if text.strip():
        # Generate speech from the text using gTTS
        os.system('espeak "{}"'.format(text))
        # Play the speech using OMXPlayer
        time.sleep(2)
        os.system('espeak "{Ready to Capture Again}"')

    else:
        print("No text detected in the image.")
        os.system('espeak "{No text detected in the image}"')
        time.sleep(1)
        os.system('espeak "{Ok Ready to Capture}"')


# Function to be called when the button is pressed
def button_pressed(channel):
    print("Button pressed!")
    capture_and_convert()

# Add event detection for the button press
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_pressed, bouncetime=300)

try:
    while True:
        # Continue running the loop
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()



