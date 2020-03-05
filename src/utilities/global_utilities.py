import random
import pandas

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

def get_random_row( pandas_df ):
    """
    Extracts a random row from a pandas dataframe and exports it.
    Returns None if there are no rows.
    """
    if len(pandas_df)==0:
        return None
    
    try:
        # If a dataframe was passed in
        if type(pandas_df)==pandas.core.frame.DataFrame:
            chosen_index = random.choice( pandas_df.index )
            return pandas_df.loc[chosen_index]
        # If a list was passed in
        elif type(pandas_df)==list:
            return random.choice(pandas_df)
    except Exception as e:
        print(str(e))
        print(chosen_index)
        print(pandas_df)