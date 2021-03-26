@state_trigger("binary_sensor.kitchen_garage_entry_door == 'on'")
def entry_door_changed(value):

    if switch.kitchen_closet_light == "off":
        switch.turn_on(entity_id="switch.kitchen_closet_light")


@state_trigger("cover.garage")
@state_trigger("binary_sensor.kitchen_garage_entry_door")
def garage_changed(**kwargs):

    task.unique("garage_changed")

    if kwargs["value"] in ["on","open"]:
        if sun.sun == "below_horizon" and switch.garage_ceiling_light == "off":
            switch.turn_on(entity_id="switch.garage_ceiling_light")

    if cover.garage == "closed" and binary_sensor.kitchen_garage_entry_door == "off":
        task.sleep(900)
        if switch.garage_ceiling_light == "on":
            switch.turn_off(entity_id="switch.garage_ceiling_light")


@state_trigger("cover.garage == 'open' and sun.sun == 'below_horizon'", state_hold=900)
@task_unique("garage_open_while_dark")
def garage_open_while_dark():

    while cover.garage == "open":
        notify.mobile_app_bradys_iphone(title="Garage Alert", message="Garage is open and it is night.")
        task.sleep(900)

    