from ovos_utils import classproperty
from ovos_utils.log import LOG
from ovos_workshop.intents import IntentBuilder
from ovos_utils.process_utils import RuntimeRequirements
from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill
from ovos_bus_client.message import Message
import requests

DEFAULT_SETTINGS = {
    "log_level": "INFO"
}

class LightSkill(OVOSSkill):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.override = True
    
    @classproperty
    def runtime_requirements(self):
        # if this isn't defined the skill will
        # only load if there is internet
        return RuntimeRequirements(
            internet_before_load=False,
            network_before_load=True,
            gui_before_load=False,
            requires_internet=False,
            requires_network=True,
            requires_gui=False,
            no_internet_fallback=True,
            no_network_fallback=True,
            no_gui_fallback=True,
        )

    def initialize(self):
        self.settings.merge(DEFAULT_SETTINGS, new_only=True)
        self.settings_change_callback = self.on_settings_changed
        self.add_event('mycroft.light.play', self.handle_room_light)
        self.add_event('mycroft.color.play', self.handle_color_light)
        self.add_event('mycroft.dim.play', self.handle_dim_light)
        self.add_event('mycroft.scene.play', self.handle_scene_light)
        #self.register_entity_file('room.entity')
        #self.register_entity_file('action.entity')
        #self.register_entity_file('device.entity')
        #self.register_entity_file('lid.entity')
    
    def on_settings_changed(self):
        """This method is called when the skill settings are changed."""
        LOG.info("Settings changed!")

    @property
    def log_level(self):
        """Dynamically get the 'log_level' value from the skill settings file.
        If it doesn't exist, return the default value.
        This will reflect live changes to settings.json files (local or from backend)
        """
        return self.settings.get("log_level", "INFO")

    @intent_handler(IntentBuilder('light.intent').require('device').optionally('room').optionally('action'))
    def handle_room_light(self, message: Message):
        room_type = message.data.get('room', "alle")
        device_type = message.data.get('device')
        action_type = message.data.get('action', "aangepast")

        LOG.info(f"The room {room_type} and device {device_type} and action {action_type}.")
    
        # all rooms on/off switch       
        if room_type is "alle":
            if device_type in ("licht", "verlichting"):
                device_type = "lichten"
            if device_type in ("lamp"):
                device_type = "lampen"
            self.speak_dialog('AllLight',
                    {'room': room_type, 'device': device_type, 'action': action_type})

        # create the right lid and device name for dialog
        if device_type in ("lamp", "lampen", "lichten", "verlichting"):
            lid_type = "de"
        if device_type in ("licht"):
            lid_type = "het"

        # woonkamer specific and on/off switch
        if room_type is not "alle" and action_type is not "aangepast":
            self.speak_dialog('RoomLight',
                    {'lid': lid_type, 'room': room_type, 'device': device_type, 'action': action_type})

        # woonkamer specific toggle switch        
        if action_type is "aangepast":
            self.speak_dialog('ToggleLight',
                    {'lid': lid_type, 'room': room_type, 'device': device_type})

        url = f"http://192.168.1.187/api/manager/logic/webhook/Demo/?tag=Light"+room_type+action_type
        data = requests.get(url)
        LOG.info(f"the URL response in json {data}")

    @intent_handler(IntentBuilder('LightColor.intent').require('device').require('action').require('color').optionally('room'))
    def handle_color_light(self, message: Message):
        room_type = message.data.get('room', "alle")
        device_type = message.data.get('device')
        action_type = message.data.get('action')
        color_type = message.data.get('color')

        LOG.info(f"The room {room_type} and device {device_type} and action {action_type} and color {color_type}.")

        if room_type is "alle":
            if device_type in ("licht", "verlichting"):
                device_type = "lichten"
            if device_type in ("lamp"):
                device_type = "lampen"
            self.speak_dialog('AllColorLight',
                    {'room': room_type, 'device': device_type, 'action': action_type, 'color': color_type})
        else:
            if device_type in ("lamp", "lampen", "lichten", "verlichting"):
                lid_type = "de"
            if device_type in ("licht"):
                lid_type = "het"
            self.speak_dialog('ColorLight',
                    {'lid': lid_type, 'room': room_type, 'device': device_type, 'action': action_type, 'color': color_type})    

        url = f"http://192.168.1.187/api/manager/logic/webhook/Demo/?tag=Color"+room_type+color_type
        data = requests.get(url)
        LOG.info(f"the URL response in json {data}")

    @intent_handler(IntentBuilder('LightDim.intent').require('device').require('action').require('moreless').optionally('room'))
    def handle_dim_light(self, message: Message):
        room_type = message.data.get('room', "alle")
        device_type = message.data.get('device')
        action_type = message.data.get('action')
        moreless_type = message.data.get('moreless')

        LOG.info(f"The room {room_type} and device {device_type} and action {action_type} and dim {moreless_type}.")

        if room_type is "alle":
            if device_type in ("licht", "verlichting"):
                device_type = "lichten"
            if device_type in ("lamp"):
                device_type = "lampen"
            self.speak_dialog('AllDimLight',
                    {'room': room_type, 'device': device_type, 'moreless': moreless_type})
        else:
            if device_type in ("lamp", "lampen", "lichten", "verlichting"):
                lid_type = "de"
            if device_type in ("licht"):
                lid_type = "het"
            self.speak_dialog('DimLight',
                    {'lid': lid_type, 'room': room_type, 'device': device_type, 'moreless': moreless_type})    

        url = f"http://192.168.1.187/api/manager/logic/webhook/Demo/?tag=Dim"+room_type+moreless_type
        data = requests.get(url)
        LOG.info(f"the URL response in json {data}")

    @intent_handler(IntentBuilder('Lightscene.intent').require('scene'))
    def handle_scene_light(self, message: Message):
        scene_type = message.data.get('scene')

        LOG.info(f"The scene {scene_type}.")

        if scene_type in ("gezellig", "sfeer", "romantisch"):
            self.speak_dialog('RomanticLight',
                    {'scene': scene_type})
        if scene_type in ("werk", 'taak', "studie"):
            self.speak_dialog('TaskLight',
                    {'scene': scene_type})
        if scene_type in ("normaal"):   
            self.speak_dialog('NormalLight',
                    {'scene': scene_type})
        if scene_type in ("feest", "feestelijk"):
            self.speak_dialog('PartyLight',
                    {'scene': scene_type})
        if scene_type in ("slapen", "slaap"):
            self.speak_dialog('SleepLight',
                    {'scene': scene_type})
        if scene_type in ("ochtend"):   
            self.speak_dialog('MorningLight',
                    {'scene': scene_type})
        if scene_type in ('afsluiten'):
            self.speak_dialog('CloseLight',
                    {'scene': scene_type})
        if scene_type in ('open'):   
            self.speak_dialog('OpenLight',
                    {'scene': scene_type})
        if scene_type in ('wakker'):
            self.speak_dialog('WakeupLight',
                    {'scene': scene_type})
        
        
        url = f"http://192.168.1.187/api/manager/logic/webhook/Scene/?tag="+scene_type
        data = requests.get(url)
        LOG.info(f"the URL response in json {data}")

def create_skill():
    return LightSkill()
