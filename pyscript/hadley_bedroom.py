#######################################
# Hadley Door Event
#######################################

@state_trigger("binary_sensor.hadley_bedroom_door")
def door_event(value):

    task.unique("hadley_bedroom_door")

    """TODO implement a guest mode for hadley bedroom
    if input_boolean.emerson_bedroom_guest == "on":
        # Do nothing if guest mode is enabled
        return
    """

    if value == "on":

        light.turn_on(entity_id="light.hadley_bedroom_nightstand",kelvin=3000,transition=3,brightness=75)

        """Wait 30 minutes"""
        task.sleep(1800)

        """If still running, turn off the stuff"""
        light.turn_off(entity_id="light.hadley_bedroom_nightstand")
        switch.turn_off(entity_id="switch.hadley_bedroom_floor_fan")

    else:
        switch.turn_on(entity_id="switch.hadley_bedroom_floor_fan")
        light.turn_off(entity_id="light.hadley_bedroom_ceiling")
        light.turn_off(entity_id="light.hadley_bedroom_nightstand",transition=3)