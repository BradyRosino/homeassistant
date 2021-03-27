@state_trigger("binary_sensor.people_home")
@state_trigger("input_boolean.presence_guest")
def home_status_changed(**kwargs):

    log.info(f"kwargs: {kwargs}")

    people_home = binary_sensor.people_home
    guest_mode = input_boolean.presence_guest

    if kwargs["var_name"] == "input_boolean.presence_guest":
        notify.mobile_app_bradys_iphone(title="Guest Mode", message=f"Guest mode is now {guest_mode}")

    if people_home == "off" and guest_mode == "off":
        home_become_empty()
    elif kwargs["old_value"] == "off" and kwargs["value"] == "on":
        if people_home == "on" and guest_mode == "on":
            # Moved from one on to two on, home status did not change
            pass
        else:
            # moved from no on to one on, house became occupied
            home_became_occupied()


def home_became_empty():

    task.unique("home_status_changed")

    notify.mobile_app_bradys_iphone(title="Home Status",message="Empty house detected. The house will be set to away in 2 minutes.")

    task.sleep(120)

    climate.set_preset_mode(entity_id="climate.living_room",preset_mode="away")

    exclude_lights = [
        "light.outside_front_porch",
        "light.outside_driveway"
    ]

    include_switches = [
        "switch.emerson_bedroom_floor_fan",
        "switch.hadley_bedroom_floor_fan",
        "switch.master_bathroom_shower_fan"
    ]

    for switch_id in include_switches:
        if state.get(switch_id) == "on":
            homeassistant.turn_off(entity_id=switch_id)

    lights = state.names(domain="light")

    for light in lights:
        if state.get(light) == "on" and light not in exclude_lights:
            homeassistant.turn_off(entity_id=light)
    
    media_player_ids = state.names(domain="media_player")

    for media_player_id in media_player_ids:
        if state.get(media_player_id) in ["on","playing"]:
            media_player.turn_off(entity_id=media_player_id)
    
    fan_ids = state.names(domain="fan")

    for fan_id in fan_ids:
        if state.get(fan_id) in ["on"]:
            fan.turn_off(entity_id=fan_id)

    if cover.garage == "open":
        notify.mobile_app_bradys_iphone(title="Home Status ALERT", message="House became empty and the garage is open!")


def home_became_occupied():
    task.unique("home_status_changed")
    notify.mobile_app_bradys_iphone(title="Home Status",message="The home status is now occupied.")
    climate.set_preset_mode(entity_id="climate.living_room",preset_mode="home")