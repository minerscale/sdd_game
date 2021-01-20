import engine
import inventory
import constants
import image
import battle

# Image of a bag
bag = image.convert('images/bag.txt')

# Selected item in inventory
selected = 0

# Combination of food and armour and weapons (used for drawing)
loot_together = []

# Draw the inventory menu to the screen
def draw_inventory():
	global loot_together
	global selected
	global bag

	battle.compute_max_health()

	# Draw the inventory menu
	engine.draw_text_box(0, 0, 20, 22, fill=True, text=' I N V E N T O R Y \n===================')
	engine.draw_buf(bag.data, (14,22))

	# Sort the loot
	loot_sorted = list(battle.player_equip)
	food_sorted = []

	# Sort the food
	for ind,val in enumerate(battle.player_food.most_common()):
		if val[1] != 0:
			food_sorted.append(val[0])

	loot_together = food_sorted + loot_sorted

	# Draw the food
	for ind, val in enumerate(food_sorted):
		engine.draw_text(4, ind + 3, val[0] + ' x' + str(battle.player_food[val]))

	# Draw the loot
	for ind, val in enumerate(loot_sorted):
		if val in [battle.current_head,battle.current_body,battle.current_legs,battle.current_weapon]:
			text_to_draw = val[0] + ' [E]'
		else:
			text_to_draw = val[0]

		engine.draw_text(4, ind + len(food_sorted) + 3, text_to_draw)

	# Draw the little description box
	engine.draw_text_box(22,0,28,2,fill=True,text=' hp: ' + format(battle.player_health, ' 3d')+ ' | max: ' + format(battle.player_max_health, ' 3d'))
	if len(loot_together) != 0:
		verb = ['','']

		if loot_together[selected][1] == 'food':
			verb = ['heals ', ' hp.']
		elif loot_together[selected][1] in ['hat', 'body', 'legs']:
			verb = ['max hp + ', '.']
		elif loot_together[selected][1] == 'weapon':
			verb = ['deals ', ' damage.']

		engine.draw_text_box(22,3,28,4, fill=True, 
			text=(' ' + loot_together[selected][0]) + ':\n ' +loot_together[selected][1] + '\n ' +
				  verb[0] + str(loot_together[selected][2]) + verb[1])
		engine.plot('>', (3 + selected, 2))

	engine.draw_text_box(51,0,28,7,fill=True,
			text=(' E Q U I P P E D' + '\n' +
				  '===========================\n' +
				  ' head  : ' + battle.current_head[0] + ' +' + str(battle.current_head[2]) + 'hp\n' +
				  ' body  : ' + battle.current_body[0] + ' +' + str(battle.current_body[2]) + 'hp\n' +
				  ' legs  : ' + battle.current_legs[0] + ' +' + str(battle.current_legs[2]) + 'hp\n' +
				  ' weapon: ' + battle.current_weapon[0] + ' +' + str(battle.current_weapon[2]) + 'dmg\n'))

# Equip/eat food from inventory.
def select():
	global selected
	print (selected)

	if len(loot_together) == 0:
	    return

	# Eat food
	if loot_together[selected][1] == 'food':
	    battle.player_health = min(battle.player_health + loot_together[selected][2], battle.player_max_health)
	    battle.player_food[loot_together[selected]] -= 1
	    if (battle.player_food[loot_together[selected]] == 0):
	        selected = max(selected - 1, 0)

		# Equip armour
	elif loot_together[selected][1] == 'hat':
	    battle.current_head = loot_together[selected]
	elif loot_together[selected][1] == 'body':
	    battle.current_body = loot_together[selected]
	elif loot_together[selected][1] == 'legs':
	    battle.current_legs = loot_together[selected]
	elif loot_together[selected][1] == 'weapon':
	    battle.current_weapon = loot_together[selected]
