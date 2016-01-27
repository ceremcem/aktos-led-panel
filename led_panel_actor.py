__author__ = 'ceremcem'

from aktos_dcs import *
import MAX7219array as led_panel
import time

class LedPanel(Actor):
    def action(self):
        led_panel.init()
        self.curr_message = "aktos"
        self.prev_message = None
        while True:
            if self.curr_message != self.prev_message:
                led_panel.static_message(self.curr_message)
                self.prev_message = self.curr_message
            sleep(0.01)

    def handle_LedPanelMessage(self, msg):
        # it tooks 30 ms to show a message. so drop any messages before last message
        # in order to achieve fast response
        self.curr_message = msg["message"]

if __name__ == "__main__":
    class Test(Actor):
        def action(self):
            i = 0
            while True:
                self.send({'LedPanelMessage': {'message': "naber %d" % i}})
                i += 1
                sleep(0.5)


    LedPanel()
    Test()
    wait_all()