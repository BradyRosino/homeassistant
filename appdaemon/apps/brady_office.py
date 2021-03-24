import appdaemon.plugins.hass.hassapi as hass

class BradyOffice(hass.Hass):

	def initialize(self):
		onkyo_task = None
		scene_task = None
		self.listen_event(self.lutron_event, "lutron_caseta_button_event", area_name="Brady Office", device_name="Pico")


	def lutron_event(self,event_name, data, kwargs):

		if data["action"] != "press":
			try:
				self.onkyo_task.cancel()
			except:
				self.log('Tried to cancel a onkyo task, but none existed!', level='DEBUG')
			return
		
		if data["button_number"] == 2:
			self.create_task(self.set_scene("on"))
			#self.call_service("media_player/turn_on", entity_id="media_player.brady_office_receiver")

		elif data["button_number"] == 3:
			self.call_service("media_player/toggle", entity_id="media_player.brady_office_receiver")
		
		elif data["button_number"] == 4:
			self.create_task(self.set_scene("off"))
			#self.call_service("media_player/turn_off", entity_id="media_player.brady_office_receiver")
		
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
	
	async def set_scene(self,scene):

		if scene == "off":
			self.call_service("light/turn_off", entity_id="light.brady_office_couch", transition=5)
			self.call_service("light/turn_off", entity_id="light.brady_office_desk", transition=5)
			return

		if await self.sun_down():
			self.call_service("light/turn_on", entity_id="light.brady_office_couch", brightness=255,transition=10,color_name="royalblue")
			await self.sleep(3)
			self.call_service("light/turn_on", entity_id="light.brady_office_desk", brightness=100,transition=7,kelvin=2700)
		else:
			self.call_service("light/turn_on", entity_id="light.brady_office_desk", brightness=255,transition=7,kelvin=3200)
			self.call_service("light/turn_off", entity_id="light.brady_office_couch",transition=10)