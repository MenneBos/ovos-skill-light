from ovos_workshop.skills.ovos import OVOSSkill
from ovos_bus_client.message import Message
import os
import requests

class LightSkill(OVOSSkill):
    def __init__(self):
        super().__init__("LightSkill")

    def initialize(self):
        self.add_event('mycroft.light.play', self.handle_play_light)
        self.register_intent_file('PlayLight.intent', self.handle_play_light)
        self.register_entity_file('room.entity')

    def handle_play_light(self, message: Message):
        room_type = message.data.get('room')
        if room_type is not None:
            self.speak_dialog('PlayLight',
                              {'room': room_type})
        else:
            self.speak_dialog('PlayLight')
        #url = f"http://192.168.1.45/api/manager/logic/webhook/Terre/?tag=Light"
        url = f"http://192.168.1.187/api/manager/logic/webhook/Demo/?tag="+room_type
        data = requests.get(url)
        print(data.json())
        # self.play_audio("/home/ovos/.venvs/ovos/lib/python3.11/site-packages/skill_ovos_melody/soundbytes/As_You_Wish.mp3", False) 

def create_skill():
    return LightSkill()
