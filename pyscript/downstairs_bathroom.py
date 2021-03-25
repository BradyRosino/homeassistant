@state_trigger("binary_sensor.guest_bathroom_motion == 'on'")
def downstairs_bathroom_motion(value):

    task.unique("downstairs_bathroom_motion")

    if switch.guest_bathroom_light == 'off':
        switch.turn_on(entity_id="switch.guest_bathroom_light")
    
    task.sleep(1800)

    switch.turn_off(entity_id="switch.guest_bathroom_light")