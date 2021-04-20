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

