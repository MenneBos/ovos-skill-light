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
        self.register_entity_file('action.entity')

    def handle_play_light(self, message: Message):
        room_type = message.data.get('room')
        action_type = message.data.get('action')
        device_type = message.data.get('device')
        expression_type = "gedaan"
        
        if action_type is "give":
            action_type = "on"
        if action_type is "dark":
            action_type = "off"
        if room_type is "hang":
            room_type = "main"
        if room_type is "central":
            room_type = "main"
        if room_type is "led":
            room_type = "strip"

        if device_type in ("lamp", "lampen", "lichten", "verlichting"):
            lid_type = "de"
        if device_type in ("licht"):
            lid_type = "het"

        if room_type is " ":  # if no room is given apply to all lights
            if device_type in ("lampen", "lichten"):	
                room_type = "alle"
                lid_type = " "
            elif device_type in ("licht", "verlichting"):
                room_type = "alle"
                device_type = "lichten"
                lid_type = " "
            elif device_type in ("lamp"):
                room_type = "alle"
                device_type = "lampen"
                lid_type = " "
 

        if action_type is " ":  # if no action is given apply toggle flow
            action_type = "aangepast"
            expression_type = " "

        self.speak_dialog('LightOffOn',
                            {'lid': lid_type, 'room': room_type, 'device': device_type, 'action': action_type, 'expression':expression_type})
        
        #url = f"http://192.168.1.45/api/manager/logic/webhook/Terre/?tag=Light"
        url = f"http://192.168.1.187/api/manager/logic/webhook/Demo/?tag=Light"+room_type+action_type
        data = requests.get(url)
        print(data.json())
        # self.play_audio("/home/ovos/.venvs/ovos/lib/python3.11/site-packages/skill_ovos_melody/soundbytes/As_You_Wish.mp3", False) 

def create_skill():
    return LightSkill()
