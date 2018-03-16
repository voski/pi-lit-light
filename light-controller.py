import RPi.GPIO as GPIO


class LightController(object):
    def __init__(self, lights=[]):
        self.lights = lights
        self.setupGPIO()

    def on(self, light):
        GPIO.output(light, 1)

    def off(self, light):
        GPIO.output(light, 0)

    def setupGPIO():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.lights, GPIO.OUT)

    def cleanup():
        GPIO.cleanup()
