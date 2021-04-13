#######################################
# Morning Wakeup Nudge
#######################################

@time_trigger("cron(30 6 * * 1-5)")
def morning_nudge():

	"""Turn off the sound machine in the morning.
	If 'sleep in' is enabled, then disable it for the next night."""
	
	if binary_sensor.people_home == "on":
		if input_boolean.master_bedroom_sleep_in == "on":
			homeassistant.turn_off(entity_id="input_boolean.master_bedroom_sleep_in")
		else:
			switch.turn_off(entity_id="switch.master_bedroom_sound_machine")


#######################################
# Reminders
#######################################

@time_trigger("once(08:00:00)")
def reminders():

	if input_boolean.emerson_bedroom_guest == "on":
		notify.mobile_app_bradys_iphone(title="Home Reminder",message="Emerson bedroom guest mode is enabled.")
	
	if input_boolean.presence_guest == "on":
		notify.mobile_app_bradys_iphone(title="Home Reminder",message="Guest mode is enabled.")

#######################################
# Evening Coffee Reset
#######################################

@time_trigger("once(18:00:00)")
def coffee_reset():
	
	"""Every day at 6PM, turn off the coffee pot"""
	
	if switch.kitchen_coffee == "on":
		switch.turn_off(entity_id="switch.kitchen_coffee")
		






#######################################
# Daily at Civil Dawn
#######################################

## Daily at Civil Dawn
@time_trigger("once(sunrise - 30 min)")
def civil_dawn():

	"""Every day at civil dawn, turn off the driveway light"""
	
	if switch.outside_driveway_light == "on":
		switch.turn_off(entity_id="switch.outside_driveway_light")
	
	if light.outside_front_porch == "on":
		light.turn_off(entity_id="light.outside_front_porch")




#######################################
# Daily at Civil Dusk
#######################################

@time_trigger("once(sunset)")
def civil_dusk():

	"""Every day at civil dusk, turn on the driveway light"""
	
	if switch.outside_driveway_light == "off":
		switch.turn_on(entity_id="switch.outside_driveway_light")
	
	if light.outside_front_porch == "off":
		light.turn_on(entity_id="light.outside_front_porch")