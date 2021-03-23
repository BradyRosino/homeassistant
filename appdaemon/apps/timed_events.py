import appdaemon.plugins.hass.hassapi as hass
import datetime

#
# Timed Events App
#
# Args:
#

class TimedEvents(hass.Hass):

	def initialize(self):
		
		"""Weekdays @ 6:30 AM"""
		time = datetime.time(6, 30, 0)
		self.run_daily(self.master_wakeup_call, time, constrain_days = "mon,tue,wed,thu,fri")


		"""Turn off coffee maker if it will no longer be used"""
		time = datetime.time(18, 0, 0)
		self.run_daily(self.evening_coffee_reset, time)

		"""30 Min After Sunset"""
		self.run_at_sunset(self.sunset, offset=1800)

		"""60 Min Before Sunrise"""
		self.run_at_sunrise(self.sunrise, offset=-3600)


#######################################
# Master Bedroom Wake Up Call
#######################################

	def master_wakeup_call(self, kwargs):
		
		"""Wake up Brady & Holly at 6 am on Weekdays"""

		# Only execute the wake up call if someone is home
		if self.get_state("binary_sensor.people_home") == "off":
			return
		
		override = self.get_state("input_boolean.master_bedroom_sleep_in")

		if self.get_state("input_boolean.master_bedroom_sleep_in") == "on":
			self.turn_off("input_boolean.master_bedroom_sleep_in")
			return
		
		self.turn_off("switch.master_bedroom_sound_machine")


#######################################
# Evening Coffee Reset
#######################################

	def evening_coffee_reset(self, kwargs):
		
		"""Turn off coffee maker if it will no longer be used"""
		
		if self.get_state("switch.kitchen_coffee") == "on":
			self.turn_off("switch.kitchen_coffee")

#######################################
# 30 Min After Sunset
#######################################

	def sunset (self, kwargs):
		
		self.turn_on("switch.outside_driveway_light")


#######################################
# 60 Min Before Sunrise
#######################################

	def sunrise (self, kwargs):
		
		self.turn_off("switch.outside_driveway_light")