import appdaemon.plugins.hass.hassapi as hass
#import inovelli_red_switch

#
# Hellow World App
#
# Args:
#


class EmersonBedroom(hass.Hass):

  def initialize(self):
    
    door_timer = None
  
    #self.listen_state(self.door_changed, "binary_sensor.emerson_bedroom_door")
    self.listen_event(self.zwave_event, "zwave_js_event", node_id=47,)

  def door_changed(self, entity, attribute, old, new, kwargs):
    
    # Cancel timer, if running
    try:
      self.door_timer.cancel()
    except:
      """Tried to cancel, but no timer was running"""
      pass

    # Do nothing if a guest is present
    if self.get_state("input_boolean.emerson_bedroom_guest") == "on":
      return
    
    # Take action
    if new == "on":
      self.turn_on("light.emerson_bedroom_nightstand", brightness = 100, color_temp = 348, transition=3)
      self.door_timer = self.run_in(self.door_timeout,1800)
    elif new == "off":
      self.turn_on("switch.emerson_bedroom_floor_fan")
      self.turn_off("light.emerson_bedroom_dresser")
      self.turn_off("switch.emerson_bedroom_ceiling_light")
      self.turn_off("light.emerson_bedroom_nightstand")

  def door_timeout(self, entity, attribute, old, new, kwargs):

    # See Do nothing if a guest is present
    if self.get_state("input_boolean.emerson_bedroom_guest") == "on":
      return
    
    self.call_service("notify/mobile_app_bradys_iphone", title = "DEBUG", message = "Emerson bedroom door timeout")

  def zwave_event(self,event_name, data, kwargs):

    #self.log(data)
    if data["property_key"] == "003" and data["value"] == "KeyPressed":

      # FAVORITE / CONFIG BUTTON
      
      self.call_service("notify/mobile_app_bradys_iphone", title = "DEBUG", message = "Emerson favorite button")
      self.call_service("light/turn_off",entity_id="light.emerson_bedroom_ceiling")
      self.call_service("light/turn_on", entity_id="light.emerson_bedroom_nightstand", brightness=150, color_name="pink", transition=5)
      self.call_service("light/turn_on", entity_id="light.emerson_bedroom_dresser", brightness=150, color_name="purple", transition=5)

    elif data["property_key"] == "002" and (data["value"] == "KeyHeldDown" or data["value"] == "KeyPressed2x"):
      
      # UP HELD or UP x2
      
      self.run_sequence([
        {'light/turn_on': {'entity_id': 'light.emerson_bedroom_dresser', 'brightness': '255', 'kelvin': '2700', 'transition':'3'}},
        {'light/turn_on': {'entity_id': 'light.emerson_bedroom_nightstand', 'brightness': '255', 'kelvin': '2700', 'transition':'3'}},
        {'sleep': 3},
        {'light/turn_on': {'entity_id': 'light.emerson_bedroom_ceiling'}},
      ])
      
    elif data["property_key"] == "001" and (data["value"] == "KeyHeldDown" or data["value"] == "KeyPressed2x"):

      # DOWN HELD or DOWN x2
      self.call_service("light/turn_off", entity_id="light.emerson_bedroom_nightstand", transition=3)
      self.call_service("light/turn_off", entity_id="light.emerson_bedroom_dresser", transition=3)
      self.call_service("light/turn_off",entity_id="light.emerson_bedroom_ceiling")


  def button_changed(self, entity, attribute, old, new, kwargs):

    #self.log(new)
    if new == '':
      return
    
    # Cancel any running timers
    try:
      self.cancel_timer(self.timer_library[entity])
    except KeyError:
      self.log('Tried to cancel a timer for {}, but none existed!'.format(entity), level='DEBUG')


    # Single Tap
    if new == 'single':

      if self.get_state("light.emerson_bedroom_nightstand") == 'off':

        # Only set light timeout if not in Emerson guest mode
        if self.get_state("input_boolean.emerson_bedroom_guest") == 'off':
          self.timer_library[entity] = self.run_in(self.light_timeout,delay=300,entity_name=entity)
        
        self.call_service("light/turn_on", entity_id = "light.emerson_bedroom_nightstand", brightness = 100)
        
      else:
        self.call_service("light/turn_off", entity_id = "light.emerson_bedroom_nightstand")
    
    # Double Tap
    if new == 'double':

      # Only set light timeout if not in Emerson guest mode
      if self.get_state("input_boolean.emerson_bedroom_guest") == 'off':
          self.timer_library[entity] = self.run_in(self.light_timeout,delay=300,entity_name=entity)
      
      self.call_service("light/turn_on", entity_id = "light.emerson_bedroom_nightstand", effect = 'colorloop', brightness = 150)

  def light_timeout(self, kwargs):

    if self.get_state("light.emerson_bedroom_nightstand") != 'off':
      self.call_service("light/turn_off", entity_id = "light.emerson_bedroom_nightstand")


  def zwave_scene_activated(self,event_name, data, kwargs):
    
    node_id = data["node_id"]
    scene_id = data["scene_id"]
    scene_value = data["scene_value_id"]
    
    self.log('Node: {}'.format(node_id))
    self.log('Scene: {}'.format(scene_id))
    self.log('Value: {}'.format(scene_value))
    
    
    if scene_id == 3: # Config button
      if scene_value == 1: # Pressed 1 time
        self.call_service("light/turn_on", entity_id = "light.emerson_bedroom_nightstand", effect = 'colorloop', brightness = 150)
    elif scene_id == 1: # Down button
      if scene_value == 2: # Held Down
        self.call_service("light/turn_off", entity_id = "light.emerson_bedroom_nightstand")

    #if scene == inovelli_red_switch.hold_off:
    #  self.call_service("switch/turn_off", entity_id = "switch.emerson_bedroom_floor_fan")
    #  self.call_service("light/turn_off", entity_id = "light.emerson_bedroom_dresser")
    #  self.call_service("switch/turn_off", entity_id = "switch.emerson_bedroom_ceiling_light")
    #  self.call_service("light/turn_off", entity_id = "light.emerson_bedroom_nightstand")
    #
    #if scene == inovelli_red_switch.favorite:
    #  self.call_service("switch/toggle", entity_id = "switch.emerson_bedroom_floor_fan")

        


  def door_still_open(self, kwargs):
    #friendly_name = self.get_state(kwargs['entity_name'], attribute='friendly_name')
    #message = "{} has been open for more than 1800 seconds.".format(friendly_name)
    #liself.call_service("notify/mobile_app_bradys_iphone", title = "DEBUG", message = message)
    self.call_service("switch/turn_off", entity_id = "switch.emerson_bedroom_floor_fan")
    self.call_service("light/turn_off", entity_id = "light.emerson_bedroom_dresser")
    self.call_service("switch/turn_off", entity_id = "switch.emerson_bedroom_ceiling_light")
    self.call_service("light/turn_off", entity_id = "light.emerson_bedroom_nightstand")
    