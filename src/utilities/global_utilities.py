import random

equip_regions = ['head', 'face', 'chest', 'legs', 
                 'hands', 'feet', 'finger', 'neck', 
                 'held_2h', 'held_rh', 'held_lh', 
                 'back','ammo']

armor_types = ['cloth', 'light', 'medium', 'heavy']

# Object condition definitions
object_conditions = ['perfect', 'pristine', 'worn', 'damaged', 'broken']
object_conditions_numerical = [0, 1, 2, 3, 4]
object_conditions_dict = {'perfect': 0, 'pristine': 1,
                         'worn': 2, 'damaged':3, 'broken':4}
object_conditions_dict_inv = {v: k for k, v in object_conditions_dict.items()}


# Roll a number of dice with modifiers
def roll( roll, modifier=0 ):
    """
    Simulates a roll of a die with a modifier.
    
    'die' syntax is: XdY+Z
    """
    
    dice_count = int( roll.split('d')[0] )
    
    # Extract number of sides on the dice and the included roll modifier
    if '+' in roll:
        sides = int( roll.split('d')[1].split('+')[0] )
        roll_modifier = int( roll.split('d')[1].split('+')[1] )
    elif '-' in roll:
        sides = int( roll.split('d')[1].split('-') )
        roll_modifier = int( roll.split('d')[1].split('-')[1] )
    else:
        sides = int( roll.split('d')[1] )
        roll_modifier = 0
        
    # Begin the result at both modifiers being added together
    roll_result = modifier + roll_modifier
    # Add all of the randomly generated rolls
    for i in range(dice_count):
        roll_result += random.randint(1,sides)
        
    return roll_result

def get_modifier( stat ):
    return int( (stat-10)/2 )