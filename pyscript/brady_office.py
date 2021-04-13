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
        if media_player.brady_office_receiver == "on":
            # Sonos stopped, set back to pc input
            media_player.select_source(entity_id="media_player.brady_office_receiver",source="pc")



@state_trigger("media_player.brady_office_receiver == 'on'")
def brady_office_receiver_powered_on():

    if media_player.brady_office_receiver.source == "Sonos" and media_player.brady_office_sonos != "playing":
        media_player.select_source(entity_id="media_player.brady_office_receiver",source="pc")

@state_trigger("media_player.brady_office_receiver.source")
def brady_office_receiver_source_changed(**kwargs):
    value = media_player.brady_office_receiver.source
    log.info(value)
    if value == "Computer":
        media_player.volume_set(entity_id="media_player.brady_office_receiver",volume_level=0.5)
    elif value == "Switch":
        media_player.volume_set(entity_id="media_player.brady_office_receiver",volume_level=0.3)
    elif value == "Playstation":
        media_player.volume_set(entity_id="media_player.brady_office_receiver",volume_level=0.3)



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

