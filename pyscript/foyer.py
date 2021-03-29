from datetime import datetime
from datetime import timedelta

@state_trigger("binary_sensor.foyer_motion == 'on'")
@time_active("range(sunset - 20min, sunrise + 20min)")
def foyer_motion():

    if light.kitchen_island_lights == "off":
        last_changed = datetime.utcnow().replace(tzinfo=None) - datetime.fromisoformat(str(light.kitchen_island_lights.last_changed)).replace(tzinfo=None)

        if last_changed > timedelta(minutes=2):
            light.turn_on(entity_id="light.kitchen_island_lights",brightness=75,transition=2)