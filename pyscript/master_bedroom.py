@event_trigger("sensor.master_bathroom_shower_humidity")
def master_bathroom_humidity_changed(value):

    if float(value) > 60.00:
        if switch.master_bathroom_shower_fan == "off":
            switch.turn_on(entity_id="switch.master_bathroom_shower_fan")
    elif float(value) < 55.00:
        if switch.master_bathroom_shower_fan == "on":
            switch.turn_off(entity_id="switch.master_bathroom_shower_fan")