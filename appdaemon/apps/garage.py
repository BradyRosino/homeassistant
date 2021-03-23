import appdaemon.plugins.hass.hassapi as hass

#
# Hadley Bedroom App
#
# Args:
#

class Garage(hass.Hass):

  def initialize(self):
    
    self.door_timer_library = {}
    self.listen_state(self.door_changed, "binary_sensor.kitchen_garage_entry_door")
    self.listen_state(self.door_changed, "cover.garage")

  def door_changed(self, entity, attribute, old, new, kwargs):
    
    try:
      self.cancel_timer(self.door_timer_library[entity])
    except KeyError:
      self.log('Tried to cancel a timer for {}, but none existed!'.format(entity), level='DEBUG')      
    
    # TODO: Add conditions to only turn on if garage is actually dark enough
    
    if (new == "on" or new == "open") and self.sun_down():
      self.turn_on("switch.garage_ceiling_light")
    elif new == "off" or new == "closed":
      self.door_timer_library[0] = self.run_in(self.timeout,delay=900,entity_name=entity)


  def timeout(self, kwargs):
    #friendly_name = self.get_state(kwargs['entity_name'], attribute='friendly_name')
    #message = "{} has been open for more than 1800 seconds.".format(friendly_name)
    #self.call_service("notify/mobile_app_bradys_iphone", title = "DEBUG", message = message)
    self.call_service("switch/turn_off", entity_id = "switch.garage_ceiling_light")
