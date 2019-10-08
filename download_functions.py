"""download_functions.py - This file contains all the functions for the 
download_memorybook_photos.py application

"""
import os
import urllib.request as req
import logging
import requests
import pandas as pd

log = logging.getLogger(__name__)


def open_excel_file(file_name):
    """ Open the excel file and put it into a pandas dataframe. """
    photo_df = pd.read_excel(file_name)
    return photo_df

def get_teams(data_frame):
    """Get the distinct team names from the file and create a directory for each one."""
    
    #Set the Team Names
    team_names = data_frame.Team.unique()
    
    return team_names

def create_team_directory(team, BASE_DIRECTORY):
    """create a directory for each team.""" 
    try:
        log.info('Creating directory for team {}'.format(team))
        os.mkdir(BASE_DIRECTORY+'/'+team)
    except:
        pass

def filter_team_data(team, data):
    """Create a data frame with just the data for a given team"""
    log.debug('Creating dataframe for {}\n'.format(team))

    team_rows = data.loc[data['Team'] == team]

    return team_rows

def get_players(data_frame, team):
    """Get all the players for a given team."""
    log.debug('Creating player data frame for {}\n'.format(team))
    player_list = data_frame.Player_Name.unique()

    return player_list
    
def create_player_directory(team, player, BASE_DIRECTORY):
    """Create Directories for those players"""
    player_dir = str(team + '/' + str(player))
    log.info('Creating directory for {}.'.format(player))
    os.mkdir(BASE_DIRECTORY + '/' + player_dir)


def get_player_data(player, data):
    """Get the data for the specific player"""
    #get the pictures for each player
    player_data = data.loc[data['Player_Name'] == player].dropna(axis='columns')

    return player_data

def get_player_picture_data(data):
    """Getting the pictures for the specifid player and putting them in their dirctory"""
    column_count = len(data.columns) - 3
    first_col = 1

    #list of photos for the player.
    url_list = []

    log.info('Downloading Photos for {}.'.format(data['Player_Name'].values[0]))
    while first_col < column_count:
        col = 'Photo'+str(first_col)
        url_list.append(data[col].values[0])

        first_col += 1
        
    return url_list        


def parse_photo_id(photo_url):
    """Parse the url provided to strip out the photo id"""
    photo_id = photo_url.split("/")[5]
    return photo_id


def download_photos(url_base, v_photo, pname):
    """Download the large format of the photo from flick """
    
    photo_id = parse_photo_id(v_photo)
    params = ''
    
    url = url_base + photo_id

    log.debug('Getting response for', url+photo_id)
    response = requests.get(url, params=params)
   
    data = response.json()

    sizes = data['sizes']

    photo_size_list = sizes['size']
    for item in photo_size_list:
        if item['label'] == 'Original':
            log.debug('Retrieving Photo!', item['source'])
            req.urlretrieve(item['source'], pname)
