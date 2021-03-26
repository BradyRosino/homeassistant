@state_trigger("input_select.family_room_scene != 'Set a scene...'")
def scene_family_room(value):

    task.unique("scene_family_room")
    
    # Reset scene selector
    input_select.select_first(entity_id="input_select.family_room_scene")
    
    if value == "Max Brightness":
    
	    light.turn_on(entity_id="light.family_room_window",brightness=255,transition=3,kelvin=3500)
	    light.turn_on(entity_id="light.family_room_couch",brightness=255,transition=3,kelvin=3500)
	    light.turn_on(entity_id="light.family_room_end_table",brightness=255,transition=3,kelvin=3500)
	    task.sleep(3)
	    light.turn_on(entity_id="light.family_room_bookshelf_huegroup",brightness=255,transition=3,kelvin=3500)
    
    elif value == "Good Morning":

        light.turn_on(entity_id="light.family_room_window",brightness=100,transition=10,kelvin=2900)
        light.turn_on(entity_id="light.family_room_end_table",brightness=100,transition=10,kelvin=2900)

    elif value == "Watch TV":
    
        switch.turn_off(entity_id="switch.kitchen_closet_light")
        light.turn_off(entity_id="light.kitchen_island_lights",transition=7)
        light.turn_off(entity_id="light.kitchen_table_lights",transition=7)
        light.turn_on(entity_id="light.kitchen_main_lights",brightness=100,transition=10)
        light.turn_on(entity_id="light.family_room_bookshelf_huegroup",brightness=150,transition=10,color_name="royalblue")
        task.sleep(2)
        light.turn_on(entity_id="light.family_room_window",brightness=255,transition=10,kelvin=3000)
        light.turn_on(entity_id="light.family_room_couch",brightness=255,transition=10,kelvin=3000)
        light.turn_on(entity_id="light.family_room_end_table",brightness=255,transition=10,kelvin=3000)
        
        
        
    elif value == "Watch Movie":
    
        switch.turn_off(entity_id="switch.kitchen_closet_light")
        light.turn_off(entity_id="light.kitchen_island_lights", transition=10)
        light.turn_off(entity_id="light.kitchen_table_lights", transition=10)
        light.turn_off(entity_id="light.kitchen_main_lights", transition=10)
        task.sleep(2)
        light.turn_on(entity_id="light.family_room_bookshelf_huegroup",brightness=100,transition=10,color_name="royalblue")
        light.turn_off(entity_id="light.family_room_window",transition=10)
        light.turn_off(entity_id="light.family_room_couch",transition=10)
        light.turn_off(entity_id="light.family_room_end_table",transition=10)