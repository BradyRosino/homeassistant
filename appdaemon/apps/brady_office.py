import appdaemon.plugins.hass.hassapi as hass

class BradyOffice(hass.Hass):

	def initialize(self):
		onkyo_task = None
		self.listen_event(self.lutron_event, "lutron_caseta_button_event", area_name="Brady Office", device_name="Pico")


	def lutron_event(self,event_name, data, kwargs):

		if data["action"] != "press":
			try:
				self.onkyo_task.cancel()
			except:
				self.log('Tried to cancel a onkyo task, but none existed!', level='DEBUG')
			return
		
		if data["button_number"] == 2:
			self.call_service("media_player/turn_on", entity_id="media_player.brady_office_receiver")

		elif data["button_number"] == 3:
			self.call_service("media_player/toggle", entity_id="media_player.brady_office_receiver")
		
		elif data["button_number"] == 4:
			self.call_service("media_player/turn_off", entity_id="media_player.brady_office_receiver")
		
		elif data["button_number"] == 5:
			self.onkyo_task = self.create_task(self.onkyo_volume_adjust("media_player/volume_up"))

		elif data["button_number"] == 6:
			self.onkyo_task = self.create_task(self.onkyo_volume_adjust("media_player/volume_down"))


	async def onkyo_volume_adjust(self,service):
		count = 0
		while (count < 20):
			count = count + 1
			await self.sleep(.3)
			self.call_service(service,entity_id="media_player.brady_office_receiver")