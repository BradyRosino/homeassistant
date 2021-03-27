#######################################
# Emerson Door Event
#######################################

@state_trigger("binary_sensor.emerson_bedroom_door")
def door_event(value):

    task.unique("emerson_door_event")

    if input_boolean.emerson_bedroom_guest == "on":
        # Do nothing if guest mode is enabled
        return

    if value == "on":

        light.turn_on(entity_id="light.emerson_bedroom_nightstand",kelvin=3000,transition=3,brightness=75)

        """Wait 30 minutes"""
        task.sleep(1800)

        """If still running, turn off the stuff"""
        light.turn_off(entity_id="light.emerson_bedroom_nightstand")
        switch.turn_off(entity_id="switch.emerson_bedroom_floor_fan")

    else:
        switch.turn_on(entity_id="switch.emerson_bedroom_floor_fan")
        light.turn_off(entity_id="light.emerson_bedroom_ceiling")
        light.turn_off(entity_id="light.emerson_bedroom_nightstand",transition=3)
        task.sleep(3)
        light.turn_off(entity_id="light.emerson_bedroom_dresser",transition=5)

#######################################
# Emerson Ceiling Light Z-Wave Scenes
#######################################

@event_trigger("zwave_js_event", "node_id == 47")
def zwave_event(**kwargs):

    if kwargs["property_key"] == "003" and kwargs["value"] == "KeyPressed":
        # FAVORITE / CONFIG BUTTON

        light.turn_off(entity_id="light.emerson_bedroom_ceiling")
        light.turn_on(entity_id="light.emerson_bedroom_nightstand", brightness=150, color_name="pink", transition=5)
        light.turn_on(entity_id="light.emerson_bedroom_dresser", brightness=150, color_name="purple", transition=5)

    elif kwargs["property_key"] == "002" and (kwargs["value"] == "KeyHeldDown" or kwargs["value"] == "KeyPressed2x"):

        # UP HELD or UP x2

        light.turn_on(entity_id="light.emerson_bedroom_dresser", brightness=255, kelvin=2700, transition=3)
        light.turn_on(entity_id="light.emerson_bedroom_nightstand", brightness=255, kelvin=2700, transition=3)
        task.sleep(3)
        light.turn_on(entity_id="light.emerson_bedroom_ceiling")


    elif kwargs["property_key"] == "001" and (kwargs["value"] == "KeyHeldDown" or kwargs["value"] == "KeyPressed2x"):

        # DOWN HELD or DOWN x2
        light.turn_off(entity_id="light.emerson_bedroom_nightstand", transition=3)
        light.turn_off(entity_id="light.emerson_bedroom_dresser", transition=3)
        light.turn_off(entity_id="light.emerson_bedroom_ceiling")