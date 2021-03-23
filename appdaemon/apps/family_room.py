import appdaemon.plugins.hass.hassapi as hass

class FamilyRoom(hass.Hass):
  
	def initialize(self):
		family_room_scene = None
		#self.listen_state(self.basement_lights, "light.basement_stairs")
		#self.listen_state(self.family_room_scene,"input_select.family_room_scene", old="Set a scene...")
		#self.listen_state(self.cancel_scene,"input_boolean.appdaemon_debug")

	def family_room_scene(self, entity, attribute, old, new, kwargs):
	
		"""Reset scene selector"""
		
		self.call_service("input_select/select_first", entity_id="input_select.family_room_scene")
		
		"""Set the correct scene"""
		
		if new == "Max Brightness":
			handle = self.run_sequence("sequence.family_room_max_brightness")
		elif new == "Watch TV":
			self.log("Calling the async function")
			self.family_room_scene = self.create_task(self.scene_family_room_watch_tv())

	def cancel_scene(self, entity, attribute, old, new, kwargs):
		self.family_room_scene.cancel()

	async def scene_family_room_watch_tv(self):	
		
		self.turn_off(entity_id="switch.kitchen_closet_light")
		self.turn_off(entity_id="light.kitchen_island_lights",transition=7)
		self.turn_off(entity_id="light.kitchen_table_lights",transition=7)
		self.turn_on(entity_id="light.kitchen_main_lights",brightness=100,transition=10)
		self.turn_on(entity_id="light.family_room_bookshelf_huegroup",brightness=150,transition=10,color_name="royalblue")
		await self.sleep(10)
		self.turn_on(entity_id="light.family_room_window",brightness=255,transition=10,kelvin=3000)
		self.turn_on(entity_id="light.family_room_couch",brightness=255,transition=10,kelvin=3000)
		self.turn_on(entity_id="light.family_room_end_table",brightness=255,transition=10,kelvin=3000)