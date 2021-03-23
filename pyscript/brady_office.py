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

#@event_trigger("lutron_caseta_button_event", "area_name == 'Brady Office' and device_name == 'Pico'")
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
            count = count + 1
            task.sleep(.3)
            service.call("media_player",action, entity_id="media_player.brady_office_receiver")
