__author__ = 'ceremcem'

from aktos_dcs import *
from led_panel_actor import LedPanel

if __name__ == "__main__":
    print "Led panel server started listening"
    print "Send 'LedPanelMessage: {message: ...}' to display a message."
    ProxyActor()
    LedPanel()
    wait_all()
