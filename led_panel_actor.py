__author__ = 'ceremcem'

from aktos_dcs import *
import MAX7219array as led_panel

class LedPanel(Actor):
    def action(self):
        led_panel.init()

    def handle_LedPanelMessage(self, msg):
        led_panel.static_message(msg["message"])


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