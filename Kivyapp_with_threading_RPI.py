
import threading
from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from datetime import datetime
import adafruit_rfm9x
from gpiozero import MotionSensor
import sys
import time
from gpiozero import MotionSensor
import subprocess

Config.set('graphics', 'resizable', '0')
# fix the width of the window
Config.set('graphics', 'width', '770')
# fix the height of the window
Config.set('graphics', 'height', '465')

Builder.load_string("""

<MySec>:
    orientation: 'vertical'
    size: root.width, root.height
    rotation: 90

    Label:
        text: 'Master Wall Mount'
        font_size: 45

    Button:
        id: kv_sec
        text: root.seconds_string
        font_size: 80


    Button:
        id: button2
        text: 'Button 2'
        on_press: 

    Button:
        id: button3
        text: 'Button 3' 


""")


def turn_on():
    CONTROL = "vcgencmd"
    CONTROL_UNBLANK = [CONTROL, "display_power", "1"]
    subprocess.call(CONTROL_UNBLANK)


def turn_off():
    CONTROL = "vcgencmd"
    CONTROL_BLANK = [CONTROL, "display_power", "0"]
    subprocess.call(CONTROL_BLANK)


def pirsensor():
    pir = MotionSensor(4)
    # dhtDevice = adafruit_dht.DHT22(board.D23)

    while True:
        if pir.motion_detected:
            turn_on()
            print("Motion Detected!")
            time.sleep(10.0)
            print("sleeping for 10 secs")

        else:
            turn_off()
            print("No Motion Detected!")


t1 = threading.Thread(target=pirsensor)


# t2 = threading.Thread(target=red)

class MySec(BoxLayout):
    seconds_string = StringProperty('')


class TestThreadApp(App):
    print("Running Thread for PIR Sensor")
    t1.start()

    def build(self):
        Clock.schedule_interval(lambda dt: self.update_time(), 1)
        return MySec()

    def update_time(self):
        self.root.seconds_string = datetime.now().strftime("%H:%M:%S")


TestThreadApp().run()



