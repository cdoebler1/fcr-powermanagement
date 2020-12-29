from mycroft import MycroftSkill, intent_file_handler
import subprocess
import os


class Winston_reporting(MycroftSkill):
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
        power = os.system('/home/pi/mycroft-core/skills/'
                          'fcr-powermanagement.cdoebler1/get_power.sh')
        self.speak("My power level is good.")
        print(power)
#        power = power.communicate()[0].decode('ascii')[9:-7]
#        self.speak("I am at {} percent power."
#                   .format(power))

    def stop(self):
        pass


def create_skill():
    return Winston_reporting()
