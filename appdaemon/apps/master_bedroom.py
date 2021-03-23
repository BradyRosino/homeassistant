import appdaemon.plugins.hass.hassapi as hass

#
# Master Bedroom App
#
# Args:
#

class MasterBedroom(hass.Hass):

  def initialize(self):
    
    self.listen_state(self.shower_humidity_changed, "sensor.master_bathroom_shower_humidity")

  def shower_humidity_changed(self, entity, attribute, old, new, kwargs):

    if float(new) > 60.00:
      if self.get_state("switch.master_bathroom_shower_fan") == 'off':
        self.log('New shower humidity {}, turning on fan'.format(float(new)), level='INFO')
        self.call_service("switch/turn_on", entity_id = "switch.master_bathroom_shower_fan")
    elif float(new) < 50.00:
      if self.get_state("switch.master_bathroom_shower_fan") == 'on':
        self.log('New shower humidity {}, turning off fan'.format(float(new)), level='INFO')
        self.call_service("switch/turn_off", entity_id = "switch.master_bathroom_shower_fan")