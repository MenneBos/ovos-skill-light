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
        self.add_event('mycroft.room.play', self.handle_room_light)
        #self.add_event('mycroft.all.play', self.handle_all_light)
        #self.add_event('mycroft.toggle.play', self.handle_toggle_light)
        self.register_entity_file('room.entity')
        self.register_entity_file('action.entity')
        self.register_entity_file('device.entity')
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

    @intent_handler("RoomLight.intent")
    def handle_room_light(self, message: Message):
        room_type = message.data.get('room')
        action_type = message.data.get('action')
        device_type = message.data.get('device')
        
        if device_type in ("lamp", "lampen", "lichten", "verlichting"):
            lid_type = "de"
        if device_type in ("licht"):
            lid_type = "het"

        if room_type is not None and action_type is not None: # switch room light on/off
            self.speak_dialog('RoomLight',
                    {'lid': lid_type, 'room': room_type, 'device': device_type, 'action': action_type})
        else:
            if room_type is not None:  # action is None so toggle the room light
                self.speak_dialog('ToggleLight',
                        {'lid': lid_type, 'room': room_type, 'device': device_type})
            else:
                if device_type in ("licht", "verlichting"):
                    device_type = "lichten"
                if device_type in ("lamp"):
                    device_type = "lampen"
                room_type = "alle"
                self.speak_dialog('AllLight',
                    {'room': room_type, 'device': device_type, 'action': action_type})

        url = f"http://192.168.1.187/api/manager/logic/webhook/Demo/?tag=Light"+room_type+action_type
        data = requests.get(url)
        print(data.json())

    #url = f"http://192.168.1.45/api/manager/logic/webhook/Terre/?tag=Light"

def create_skill():
    return LightSkill()
