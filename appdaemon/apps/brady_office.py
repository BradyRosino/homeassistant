import appdaemon.plugins.hass.hassapi as hass

#
# Brady Office automations
#
# Args:
#


class BradyOffice(hass.Hass):

  def initialize(self):

    #self.listen_state(self.handle_cube_action, "sensor.brady_office_cube_action", old = "")
    self.listen_event(self.lutron_event, "lutron_caseta_button_event", area_name="Brady Office", device_name="Pico", action="press")
    #self.listen_state(self.sonos_event, "media_player.brady_office_sonos")

  #def sonos_event(self, entity, attribute, old, new, kwargs):
    
    #if new == 'playing' and old != 'playing':
    #  if self.get_state("media_player.brady_office_receiver") != 'on':
    #    self.log('Brady Office Receiver is off while Sonos is playing, turning on receiver')
    #    self.call_service("media_player/turn_on", entity_id = 'media_player.brady_office_receiver')
    #  self.log('Brady Office Sonos is now playing, switching to CD input')
    #  self.call_service("media_player/select_source", entity_id = "media_player.brady_office_receiver", source = "cd")
    #elif new != 'playing' and old == 'playing' :
    #  self.log('Brady Office Sonos is now stopped, switching to PC source')
    #  self.call_service("media_player/select_source", entity_id = "media_player.brady_office_receiver", source = "pc")
      

  def lutron_event(self,event_name, data, kwargs):
  
    self.log(data)

    if data["button_number"] == 3: # FAVORITE

      # Get SUN state to decide which scene to set
      sun = self.render_template("{{ states('sun.sun') }}")

      if sun == 'above_horizon':
        self.log("The sun is {}, setting work lights".format(sun))
        self.call_service("scene/turn_on", entity_id="scene.brady_office_day_work", transition=10)
        #self.call_service("light/turn_on", entity_id="light.brady_office_desk", transition=5, brightness=255, kelvin=4800)
        #self.call_service("light/turn_off", entity_id="light.brady_office_couch", transition=10)
      else:
        self.log("The sun is {}, setting evening lights".format(sun))
        self.call_service("scene/turn_on", entity_id="scene.brady_office_late_night", transition=10)
        #self.call_service("light/turn_on", entity_id="light.brady_office_desk", transition=8, brightness=150, kelvin=3200)
        #self.call_service("light/turn_on", entity_id="light.brady_office_couch", transition=8, brightness=255, kelvin=3200)
  
    #self.log('payload: {}'.format(data))
    #if data["button_number"] == 2: # ON
      #self.call_service("media_player/turn_on", entity_id = "media_player.brady_office_receiver")
      #self.call_service("media_player/volume_set", entity_id = "media_player.brady_office_receiver", volume_level=0.25)
    #elif data["button_number"] == 3: #$ FAVORITE
      #self.call_service("light/toggle", entity_id = "light.brady_office_desk")
    #elif data["button_number"] == 4: # OFF
      #self.call_service("media_player/turn_off", entity_id = "media_player.brady_office_receiver")
    #elif data["button_number"] == 5: # UP
      #self.call_service("media_player/volume_up", entity_id = "media_player.brady_office_receiver")
    #elif data["button_number"] == 6: # DOWN
      #self.call_service("media_player/volume_down", entity_id = "media_player.brady_office_receiver")

  def handle_cube_action(self, entity, attribute, old, new, kwargs):
    
    self.log(new)
    
#    if new == 'flip90':
#      
#      if self.get_state("light.brady_office_desk") != 'on':
#        self.call_service("light/turn_on", entity_id = "light.brady_office_desk",brightness = 125)
#      
#      if self.get_state("media_player.brady_office_receiver") != 'on':
#        self.call_service("media_player/turn_on", entity_id = 'media_player.brady_office_receiver')
#      
#      if self.sun_down():
#        self.call_service("light/turn_on", entity_id = "light.brady_office_couch", brightness = 125, color_name = "blue")
#
#    elif new == 'flip180':
#      
#      if self.get_state("light.brady_office_desk") == 'on':
#        self.call_service("light/turn_off", entity_id = "light.brady_office_desk")
#        
#      if self.get_state("media_player.brady_office_receiver") == 'on':
#        self.call_service("media_player/turn_off", entity_id = "media_player.brady_office_receiver")
#      
#      if self.get_state("light.brady_office_couch") == 'on':
#        self.call_service("light/turn_off", entity_id = "light.brady_office_couch")
#
#    elif new == 'rotate_left':
#      volume = self.get_state("media_player.brady_office_receiver", attribute="volume_level")
#      volume = volume - 0.02
#      self.call_service("media_player/volume_set", entity_id = "media_player.brady_office_receiver", volume_level = volume)
#      #self.call_service("media_player/volume_down", entity_id = "media_player.brady_office_receiver")
#
#    elif new == 'rotate_right':
#      volume = self.get_state("media_player.brady_office_receiver", attribute="volume_level")
#      volume = volume + 0.02
#      self.call_service("media_player/volume_set", entity_id = "media_player.brady_office_receiver", volume_level = volume)
#      #self.call_service("media_player/volume_up", entity_id = 'media_player.brady_office_receiver')
#
#
#    elif new == 'shake':
#      mute_state = self.get_state("media_player.brady_office_receiver", attribute="is_volume_muted")
#      if mute_state == True:
#        self.log("Shake detected - Unmuting")
#        self.call_service("media_player/volume_mute", entity_id = 'media_player.brady_office_receiver', is_volume_muted = 'false')
#      else:
#        self.log("Shake detected - Muting")
#        self.call_service("media_player/volume_mute", entity_id = 'media_player.brady_office_receiver', is_volume_muted = 'true')
#
#    elif new == 'tap':
#      self.call_service("media_player/select_source", entity_id = "media_player.brady_office_receiver", source = "Computer")
#
#    elif new == 'slide':
#      self.log("Slide not implemnted")
#
#    elif new == 'wakeup':
#      pass
