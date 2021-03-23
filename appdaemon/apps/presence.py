import appdaemon.plugins.hass.hassapi as hass

#
# Presence automations
#
# Args:
#

class Presence(hass.Hass):

  def initialize(self):

    self.listen_state(self.home_status_changed, "binary_sensor.people_home")
    self.listen_state(self.guest_mode_changed, "input_boolean.presence_guest")
    

  def home_status_changed(self, entity, attribute, old, new, kwargs):
    
    guest_state = self.get_state("input_boolean.presence_guest")
    
    if new == "off" and guest_state == "off":
      self.house_became_empty()
    elif new == "on" and guest_state == "off":
      self.house_became_occupied()
    elif new == "off" and guest_state == "on":
      self.call_service("notify/mobile_app_bradys_iphone", title = "Home Status - ALERT", message = "Everybody has left but guest mode is enabled. House status to remain occupied.")


  def guest_mode_changed(self, entity, attribute, old, new, kwargs):
    
    people_home = self.get_state("binary_sensor.people_home")

    if new == "on" and people_home == "off":
      self.call_service("notify/mobile_app_bradys_iphone", title = "Home Status", message = "The status is now home due to a guest arrival.")
      self.house_became_occupied()
    elif new == "off" and people_home == "off":
      self.house_became_empty()
    else:
      self.call_service("notify/mobile_app_bradys_iphone", title = "Guest Mode", message = "Guest mode is now {}".format(new))

  def house_became_empty(self):

    garage_state = self.get_state("cover.garage")

    if garage_state == "open":
      self.call_service("notify/mobile_app_bradys_iphone", title = "Home Status - ALERT", message = "The status is now Away and the Garage is OPEN.")
    else:
      self.call_service("notify/mobile_app_bradys_iphone", title = "Home Status", message = "The status is now Away.")

    self.call_service("climate/set_preset_mode", entity_id = "climate.living_room", preset_mode = "away")
    self.call_service("light/turn_off", entity_id = "all")
    self.call_service("fan/turn_off", entity_id = "all")
    self.call_service("media_player/turn_off", entity_id = "all")
    self.turn_off("switch.emerson_bedroom_floor_fan")
    self.turn_off("switch.hadley_bedroom_floor_fan")
    self.turn_off("switch.master_bathroom_shower_fan")
    

  def house_became_occupied(self):

    self.call_service("climate/set_preset_mode", entity_id = "climate.living_room", preset_mode = "home")
      