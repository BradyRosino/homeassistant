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
