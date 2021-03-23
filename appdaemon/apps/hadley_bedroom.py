import appdaemon.plugins.hass.hassapi as hass

#
# Hadley Bedroom App
#
# Args:
#

class HadleyBedroom(hass.Hass):

  def initialize(self):
    
    self.door_timer_library = {}
    self.listen_state(self.hadley_door_changed, "binary_sensor.hadley_bedroom_door")

  def hadley_door_changed(self, entity, attribute, old, new, kwargs):
    
    try:
      self.cancel_timer(self.door_timer_library[entity])
    except KeyError:
      self.log('Tried to cancel a timer for {}, but none existed!'.format(entity), level='DEBUG')      
    
    
    if new == "on":
      self.turn_on("light.hadley_bedroom_nightstand", brightness=50)
      self.door_timer_library[entity] = self.run_in(self.door_still_open,delay=1800,entity_name=entity)
    elif new == "off":
      self.turn_on("switch.hadley_bedroom_floor_fan")
      self.turn_off("light.hadley_bedroom_nightstand")
      self.turn_off("switch.hadley_bedroom_ceiling_light")

  def door_still_open(self, kwargs):
    #friendly_name = self.get_state(kwargs['entity_name'], attribute='friendly_name')
    #message = "{} has been open for more than 1800 seconds.".format(friendly_name)
    #self.call_service("notify/mobile_app_bradys_iphone", title = "DEBUG", message = message)
    self.call_service("light/turn_off", entity_id = "light.hadley_bedroom_nightstand")
    self.call_service("switch/turn_off", entity_id = "switch.hadley_bedroom_floor_fan")
