@state_trigger("media_player.brady_office_sonos")
def brady_office_sonos(value,old_value):

    task.unique("brady_office_sonos")
    log.info(f"Office Sonos is now '{value}' and old value is '{old_value}'")
    if old_value is None:
        return
    
    if value == "playing":
        # Turn on receiver if necessary
        if media_player.brady_office_receiver != "on":
            media_player.turn_on(entity_id="media_player.brady_office_receiver")
        # Set Sonos input
        media_player.select_source(entity_id="media_player.brady_office_receiver",source="cd")

    else:
        # Sonos stopped, set back to pc input
        media_player.select_source(entity_id="media_player.brady_office_receiver",source="pc")

#######################################
# Handle Brady Office Pico Events
#######################################

@event_trigger("lutron_caseta_button_event", "area_name == 'Brady Office' and device_name == 'Pico'")
def lutron_event(**kwargs):
    
    """Listen for button release to stop any running loops"""
    if kwargs["action"] != 'press':
        onkyo_volume_adjust("stop")
        return
    
    """handle action"""

    if kwargs["button_number"] == 2:
        media_player.turn_on(entity_id="media_player.brady_office_receiver")
    
    elif kwargs["button_number"] == 4:
        media_player.turn_off(entity_id="media_player.brady_office_receiver")

    elif kwargs["button_number"] == 3:
        media_player.toggle(entity_id="media_player.brady_office_receiver")
    
    elif kwargs["button_number"] == 5:
        onkyo_volume_adjust("volume_up")

    elif kwargs["button_number"] == 6:
        onkyo_volume_adjust("volume_down")
    
    
    
def onkyo_volume_adjust(action):

    task.unique('onkyo_volume_adjust')

    if action == "volume_up" or action == "volume_down":
        count = 0
        while(count < 20):
            count += 1
            task.sleep(.3)
            service.call("media_player",action, entity_id="media_player.brady_office_receiver")


@state_trigger("sensor.brady_office_cube_action not in ['','wakeup']")
def brady_office_cube_action(value):
    """
    Handle Aqara Cube Actions

    flip90          Flip on side
    flip180         Flip upside down
    rotate_right    Rotate on z axis clockwise
    rotate_left     Rotate on z axis counter clockwise
    shake           Shake it like a polaroid
    tap             Double tap on to surface
    slide           Slide across surface
    fall            Call life alert
    """

    log.info(f"kwargs value: {value}")

    if value == "flip90":
        if sun.sun == "above_horizon":
            light.turn_on(entity_id="light.brady_office_desk",transition=3,brightness=255,kelvin=4800)
        else:
            light.turn_on(entity_id="light.brady_office_desk",transition=10,brightness=255,kelvin=2600)



    elif value == "rotate_right":
        if sun.sun == "above_horizon":
            light.turn_on(entity_id="light.brady_office_desk",transition=3,brightness=255,kelvin=4800)
        else:
            light.turn_on(entity_id="light.brady_office_desk",transition=10,brightness=255,kelvin=2600)
            light.turn_on(entity_id="light.brady_office_couch",transition=10,brightness=200,color_name="DarkCyan")


    elif value == "rotate_left":
        light.turn_off(entity_id="light.brady_office_desk",transition=3)
        light.turn_off(entity_id="light.brady_office_couch",transition=3)

