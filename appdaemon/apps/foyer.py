import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, time

class Foyer(hass.Hass):

	def initialize(self):

		self.listen_state(self.motion, "binary_sensor.foyer_motion")

	def motion(self, entity, attribute, old, new, kwargs):
	
		if new == "on":
		
			if self.sun_down():
			
				if self.get_state("light.kitchen_island_lights") == 'off':

					"""If light has been off for at least 2 minutes, turn it on. Otherwise leave off because someeone is likely walking away from the kitchen."""
					time_off = datetime.now().timestamp() - self.convert_utc(self.entities.light.kitchen_island_lights.last_changed).timestamp()
					if time_off > 120:
						self.call_service("light/turn_on", entity_id = "light.kitchen_island_lights", brightness = 55)
