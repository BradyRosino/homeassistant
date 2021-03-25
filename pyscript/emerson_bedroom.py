#######################################
# Emerson Door Event
#######################################

@state_trigger("binary_sensor.emerson_bedroom_door")
def door_event(value):

    task.unique("emerson_door_event")

    if value == "on":
        light.turn_on(entity_id="light.emerson_bedroom_nightstand",kelvin=3000,transition=3,brightness=75)

        task.sleep(1800)
        
        light.turn_off(entity_id="light.emerson_bedroom_nightstand")
        switch.turn_off(entity_id="switch.emerson_bedroom_floor_fan")

    else:
        switch.turn_on(entity_id="switch.emerson_bedroom_floor_fan")
        light.turn_off(entity_id="light.emerson_bedroom_ceiling")
        light.turn_off(entity_id="light.emerson_bedroom_nightstand",transition=3)
        task.sleep(3)
        light.turn_off(entity_id="light.emerson_bedroom_dresser",transition=5)