from mycroft import MycroftSkill, intent_file_handler
import subprocess
from threading import Thread
from time import sleep
import smbus2

DEVICE_BUS = 1
DEVICE_ADDR = 0x17


class fcr_reporting(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('fcr.temp.intent')
    def winston_temp(self, message):
        self.speak_dialog('fcr.temp')
        temp = subprocess.Popen(['/opt/vc/bin/vcgencmd', 'measure_temp'],
                                stdout=subprocess.PIPE)
        temp = temp.communicate()[0].decode('ascii')[5:-3]
        self.speak("My current core temperature is {} degrees celsius."
                   .format(temp))

    @intent_file_handler('fcr.uptime.intent')
    def winston_uptime(self, message):
        uptime = subprocess.Popen(['uptime', '-p'], stdout=subprocess.PIPE)
        uptime = uptime.communicate()[0].decode('ascii')[:-1]
        self.speak("I have been {}".format(uptime))

    @intent_file_handler('fcr.power.intent')
    def winston_power(self, message):
        bus = smbus2.SMBus(DEVICE_BUS)
        aReceiveBuf = []
        aReceiveBuf.append(0x00)
        for i in range(1, 255):
            aReceiveBuf.append(bus.read_byte_data(DEVICE_ADDR, i))
#        p = 'echo "get battery" | nc -q 0 127.0.0.1 8423'
#        pwr = pwr.communicate()[0].decode('ascii')[8:-7].strip()
#        if not pwr:
#            pwr = 100
#        self.speak("I am at {} percent power.".format(pwr))
        self.speak("Remaining power %d %%"% (aReceiveBuf[20] << 8 | aReceiveBuf[19]))

    def stop(self):
        pass


class fcr_monitoring(MycroftSkill, Thread):
    def __init__(self):
        Thread.MycroftSkill.__init__(self)

    def winston_monitor_temp(self, message):
        while True:
            temp = subprocess.Popen(['/opt/vc/bin/vcgencmd', 'measure_temp'],
                                    stdout=subprocess.PIPE)
            temp = int(temp.communicate()[0].decode('ascii')[5:-3])
            if temp > 90:
                self.speak("Core temperature is critical."
                           "Powering off immediately to mitigate damage.")
            elif temp > 80:
                self.speak("Core temperature exceeds 80 degrees celsius."
                           "Throttling core speed to reduce temperature.")
            elif temp > 70:
                self.speak("I am getting warm. My current core temperature is"
                           "{} degrees celsius.")
        sleep(30)


def create_skill():
    return fcr_reporting()
    return fcr_monitoring()
