import pandas as pd
import os, sys
import numpy as np
import json
import random

from global_utilities import *

# The available systems to use
SYSTEMS = ['dnd5e','pathfinder']

# Define relevant filepaths
UTILITIES = os.path.dirname(os.path.abspath('loading_utilities.py'))
REPO_DIR = os.path.abspath('..')
DATA_DIR = os.path.abspath('../data')
PATHFINDER_DATA_DIR = os.path.abspath('../data/Pathfinder')
DND5E_DATA_DIR = os.path.abspath('../data/DnD_5e')

### ### ### ### ### ### ### ### ###
### ### ### Loading Data ### ### ###
### ### ### ### ### ### ### ### ###

# Loading an xlsx file
def load_xlsx( fp ):
    df = pd.read_excel(fp)
    return df

def load_armor_pathfinder( ):
    fp = os.path.join( PATHFINDER_DATA_DIR, 'PathfinderArmor.xlsx')
    return load_xlsx( fp )

def load_weapons_pathfinder( ):
    fp = os.path.join( PATHFINDER_DATA_DIR, 'PathfinderWeapons.xlsx')
    return load_xlsx( fp )

def load_magicItems_pathfinder( ):
    fp = os.path.join( PATHFINDER_DATA_DIR, 'PathfinderMagicItems.xlsx')
    return load_xlsx( fp )

def load_bestiary_pathfinder( ):
    fp = os.path.join( PATHFINDER_DATA_DIR, 'PathfinderBestiary.xlsx')
    return load_xlsx( fp )

def load_spells_pathfinder( ):
    fp = os.path.join( PATHFINDER_DATA_DIR, 'PathfinderSpells.xlsx')
    return load_xlsx( fp )

def load_traits_pathfinder( ):
    fp = os.path.join( PATHFINDER_DATA_DIR, 'PathfinderTraits.xlsx')
    return load_xlsx( fp )

def load_feats_pathfinder( ):
    fp = os.path.join( PATHFINDER_DATA_DIR, 'PathfinderFeats.json')
    with open(fp, 'r') as f:
        d = f.read()
    return json.loads( d )

def load_pathfinder_data():
    data = {}
    data['armor'] = load_armor_pathfinder()
    data['weapons'] = load_weapons_pathfinder()
    data['magicItems'] = load_magicItems_pathfinder()
    data['bestiary'] = load_bestiary_pathfinder()
    data['spells'] = load_spells_pathfinder()
    data['traits'] = load_traits_pathfinder()
    data['feats'] = load_feats_pathfinder()
    return data

data = load_pathfinder_data()

### ### ### ### ### ### ### ### ###
### ### ### End Loading Specific Data ### ### ###
### ### ### ### ### ### ### ### ###

### ### ### ### ### ### ### ### ###
### ### ### Printing Data ### ### ###
### ### ### ### ### ### ### ### ###
    
def get_random_beast( cr=-1, cr_max=50, cr_min=0, 
                      return_all_that_apply=False ):
    """
    return_all_that_apply: Returns all possible options if false
    """
    beast_opt = data['bestiary']
        
    # Filter by challenge ratings
    if cr >= 0.25 and cr <= 30 :
        beast_opt = beast_opt[ beast_opt['CR']==cr ]
    if cr_max >= 0.25:
        beast_opt = beast_opt[ beast_opt['CR']<=cr_max ]
    if cr_min <= 25:
        beast_opt = beast_opt[ beast_opt['CR']>=cr_min ]
    
    if return_all_that_apply:
        return beast_opt
    else:
        return get_random_row( beast_opt )

def get_random_spell( spell_level=-1, 
                      return_all_that_apply=False ):
    """
    return_all_that_apply: Returns all possible options if false
    """
    spell_opt = data['spells']
        
    if spell_level >= 1 and spell_level <= 13 :
        spell_opt = list( np.array(spell_opt)[[str(spell_level) in i for i in spell_opt['spell_level']]] )
    
    if return_all_that_apply:
        return spell_opt
    else:
        return get_random_row( spell_opt )

def get_random_armor( armor_type='Any', 
                      armor_bonus_min=-1, 
                      return_all_that_apply=False ):
    """
    armor_type: "Shield" or "Heavy" or "Medium" or "Light"
    return_all_that_apply: Returns all possible options if false
    """
    armor_opt = data['armor']
    
    try:
        assert armor_type in ['Any', 'Shield', 'Heavy', 'Medium', 'Light']
    except:
        return None
    
    if armor_bonus_min >= 1 and armor_bonus_min <= 43 :
        armor_opt = armor_opt[ armor_opt['Armor/Shield Bonus']>=armor_bonus_min ]
    
    if not armor_type=='Any':
        armor_opt = armor_opt[ armor_opt['Type']==armor_type ]
        
    if return_all_that_apply:
        return armor_opt
    else:
        return get_random_row( armor_opt )
    
def get_random_trait( return_all_that_apply=False ):
    trait_opt = data['traits']
    
    if return_all_that_apply:
        return trait_opt
    else:
        return get_random_row( trait_opt )
    
def get_random_magicItem( cl=-1, cl_min=100, cl_max=-1, 
                         return_all_that_apply=False ):
    magicI_opt = data['magicItems']
    
    # Filter by caster level
    if cl >= 1 and cl <= 20 :
        magicI_opt = magicI_opt[ magicI_opt['CL']==cl ]
    if cl_max >= 1:
        magicI_opt = magicI_opt[ magicI_opt['CL']<=cl_max ]
    if cl_min <= 20:
        magicI_opt = magicI_opt[ magicI_opt['CL']>=cl_min ]
    
    if return_all_that_apply:
        return magicI_opt
    else:
        return get_random_row( magicI_opt )
            
def gp_str_to_int( gp_str, true_int=False ):
    if type(gp_str)==int:
        return gp_str
    
    gp_str = gp_str.replace(' ','').replace(',','')
    gp = 0
    
    if 'gp' in gp_str:
        gp_str = gp_str[0:gp_str.index('gp')+2]
        gp = int( gp_str.replace('gp','') )
    elif 'sp' in gp_str:
        gp_str = gp_str[0:gp_str.index('sp')+2]
        gp = float( gp_str.replace('sp',''))/10.0
    elif 'cp' in gp_str:
        gp = float( gp_str.replace('cp',''))/100.0
    elif '-' in gp_str:
        gp = 0
    else:
        gp = 0
        
    if true_int:
        return int(gp)
    else:
        return gp
    
def get_prices( item_gp_list, as_truthtable=True, 
                       max_price=999 ):
    new_item_gp_list = []
    for item_gp in item_gp_list:
        if as_truthtable:
            new_item_gp_list.append( gp_str_to_int(item_gp)<=max_price )
        else:
            new_item_gp_list.append( gp_str_to_int(item_gp) )
    return new_item_gp_list

def get_weapon_dice( weapon_dice_list, as_truthtable=True, 
                     min_die=1 ):
    new_weapon_dice_list = []
    for wpn_die in weapon_dice_list:
        wpn_die = wpn_die.replace('1d','').replace('P','')
        wpn_die = wpn_die.replace('S','').replace('B','')
        if wpn_die=='Varies':
            wpn_die=6
            
        try:
            wpn_die = int(wpn_die)
        except:
            print(wpn_die)
            print('get_weapon_dice Error')
            
        if as_truthtable:
            new_weapon_dice_list.append( wpn_die>=min_die )
        else:
            new_weapon_dice_list.append( wpn_die )
    return new_weapon_dice_list

def get_random_weapon( min_die=-1, melee_only=False, ranged_only=False, 
                simple=False, martial=False, advanced=False, 
                max_price=999, hands=-1, 
                return_all_that_apply=False ):
    """
    quality: From 0-10 how nice is this weapon
    return_all_that_apply: Returns all possible options if false
    """
    weapon_opt = data['weapons']
    
    if min_die >= 4:
        weapon_opt = weapon_opt[ get_weapon_dice(weapon_opt['Damage'],
                                                 min_die=min_die) ]
    
    if melee_only:
        weapon_opt = weapon_opt[ weapon_opt['Type']=='Melee' ]
    elif ranged_only:
        weapon_opt = weapon_opt[ weapon_opt['Type']=='Ranged' ]
    
    if simple:
        weapon_opt = weapon_opt[ weapon_opt['Category']=='Simple' ]
    elif martial:
        weapon_opt = weapon_opt[ weapon_opt['Category']=='Martial' ]
    elif advanced:
        weapon_opt = weapon_opt[ weapon_opt['Category']=='Advanced' ]
        
    weapon_opt = weapon_opt[ get_prices(weapon_opt['Price'], max_price=max_price) ]
    
    if hands!=-1:
        weapon_opt = weapon_opt[ str(hands) in weapon_opt['Hands'] ]
        
    if return_all_that_apply:
        return weapon_opt
    else:
        return get_random_row( weapon_opt )

def get_random_weapon_v2( min_die=-1, melee_only=False, ranged_only=False, 
                simple=False, martial=False, advanced=False, 
                max_price=999, hands=-1, 
                return_all_that_apply=False ):
    """
    quality: From 0-10 how nice is this weapon
    return_all_that_apply: Returns all possible options if false
    """
    weapon_opt = data['weapons']
    
    if min_die >= 4:
        weapon_opt = weapon_opt[ get_weapon_dice(weapon_opt['Damage'],
                                                 min_die=min_die) ]
    
    if melee_only:
        weapon_opt = weapon_opt[ weapon_opt['Type']=='Melee' ]
    elif ranged_only:
        weapon_opt = weapon_opt[ weapon_opt['Type']=='Ranged' ]
    
    if simple:
        weapon_opt = weapon_opt[ weapon_opt['Category']=='Simple' ]
    elif martial:
        weapon_opt = weapon_opt[ weapon_opt['Category']=='Martial' ]
    elif advanced:
        weapon_opt = weapon_opt[ weapon_opt['Category']=='Advanced' ]
        
    weapon_opt = weapon_opt[ get_prices(weapon_opt['Price'], max_price=max_price) ]
    
    if hands!=-1:
        weapon_opt = weapon_opt[ str(hands) in weapon_opt['Hands'] ]
        
    if return_all_that_apply:
        return weapon_opt
    else:
        return get_random_row( weapon_opt )

### ### ### ### ### ### ### ### ### ###
### ### ### END PATHFINDER ### ### ###
### ### ### ### ### ### ### ### ### ###

def print_spell( spell ):
    print('Spell Name: '+str(spell[0]))
    print('---------------------')
    print('School: '+str(spell[1]))
    print('Spell Level: '+str(spell[4]))
    print('Description: '+str(spell[17].encode('ascii', 'replace')))

def print_magic_item( magic_item ):
    print('Magic Item Name: '+magic_item['Name'])
    print('---------------------')
    print(str(magic_item['CostValue'])+'gp' )
    print('Caster Level: '+str(magic_item['CL']) )
    print('Description: '+magic_item['Description'])
    
def print_weapon( weapon ):
    print('Weapon Name: '+weapon['Name'])
    print('---------------------')
    print(str(weapon['Price'])+'' )
    print('Damage: '+str(weapon['Damage']) )
    
def print_armor( armor ):
    print('Armor Name: '+armor['Armor'])
    print('---------------------')
    print(str(armor['Cost'])+'' )
    print('AC bonus: '+str(armor['Armor/Shield Bonus']) )
    
def print_trait( trait ):
    print('Trait Name: '+trait['Trait Name'])
    print('---------------------')
    print('Benefit: '+str(trait['Benefit']) )
    print('Source: '+str(trait['Source']) )
    
def print_beast( beast ):
    print('Name: '+str(beast['Name']))
    print('---------------------')
    print('CR: '+str(beast['CR']))
    print('HP: '+str(beast['HP']))
    print('AC: '+str(beast['AC']))
    print('Treasure: '+str(beast['Treasure']))

def print_info( obj ):
    #print(type(obj))
    if type(obj)==dict or type(obj)==pandas.core.series.Series:
        obj_keys = obj.keys()
    elif type(obj)==list or type(obj)==np.ndarray:
        # check if obj is a spell
        if len(obj)==93:
            print_spell(obj)
            return
    
    # check if obj is a magic_item
    if 'CL' in obj_keys:
        print_magic_item(obj)
    # check if obj is a weapon
    elif 'Weapon Traits' in obj_keys:
        print_weapon(obj)
    # check if obj is armor
    elif 'Armor/Shield Bonus' in obj_keys:
        print_armor(obj)
    # check if obj is a trait
    elif 'Trait Name' in obj_keys:
        print_trait(obj)
    # check if obj is a beast
    elif 'CR' in obj_keys:
        print_beast(obj)
        
### ### ### ### ### ### ### ### ###
### ### ### End Printing Data ### ### ###
### ### ### ### ### ### ### ### ###