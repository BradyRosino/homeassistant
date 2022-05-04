@service
def presence_test():
    """yaml
name: Service example
description: presence_test service to trial some pyscript presence automation.
"""
    log.info(f"Testing someone leaving...")

    house_became_empty()

@state_trigger("binary_sensor.people_home == 'off'")
def house_became_empty():
    task.unique("house_became_empty")

    log.info(f"Everybody left home & no guests are present.")

    # Notify of empty house so that there is a chance to set guest mode if required
    notify.mobile_app_bradys_iphone(title="Home Status",message="Empty house detected. The house will be set to away in 2 minutes.")
    
    task.sleep(120)

    #TODO: Set climate to away temperature

    # Turn off all lights
    entities = state.names(domain='light')
    for entity_id in entities:
        # Check to see what is on before turning off lights to not flood zigbee mesh
        if state.get(entity_id) == 'on':
            # Exclude outside lights
            if "outside" in entity_id:
                log.info(f"light: {entity_id} is excluded, leaving on.")
            else:
                log.info(f"light: {entity_id} is on, turning off.")
                light.turn_off(entity_id=entity_id)

    # Turn off all fans (that are on switches)
    entities = state.names(domain='switch')
    for entity_id in entities:
        # Check to see what is on before turning off lights to not flood zigbee mesh
        if state.get(entity_id) == 'on':
            # Exclude outside lights
            if "fan" in entity_id:
                log.info(f"fan: {entity_id} is on, turning off.")
                switch.turn_off(entity_id=entity_id)
    
    media_player.media_stop(entity_id="all")
    media_player.turn_off(entity_id="all")
    fan.turn_off(entity_id="all")
    switch.turn_on(entity_id="switch.actions_hadley_camera")
    switch.turn_on(entity_id="switch.actions_emerson_camera")
    switch.turn_on(entity_id="switch.record_motion_hadley_camera")
    switch.turn_on(entity_id="switch.record_motion_emerson_camera")

    if cover.garage == "on":
        notify.mobile_app_bradys_iphone(title="Home Status ALERT",message="House became empty and the garage is open!")