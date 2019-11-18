import pandas as pd
import os, sys
import numpy as np
import json

# The available systems to use
SYSTEMS = ['dnd5e','pathfinder']

# Define relevant filepaths
UTILITIES = os.path.dirname(os.path.abspath('loading_utilities.py'))
REPO_DIR = os.path.abspath('..')
DATA_DIR = os.path.abspath('../data')
PATHFINDER_DATA_DIR = os.path.abspath('../data/Pathfinder')
DND5E_DATA_DIR = os.path.abspath('../data/DnD_5e')

# Loading an xlsx file
def load_xlsx( fp ):
    df = pd.read_excel(fp)
    return df

### ### ### ### ### ### ### ### ###
### ### ### PATHFINDER ### ### ###
### ### ### ### ### ### ### ### ###

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

### ### ### ### ### ### ### ### ### ###
### ### ### END PATHFINDER ### ### ###
### ### ### ### ### ### ### ### ### ###