#download_memorybook_photos.py
'''
This will import a spreadsheet from a google form with a list of players
and photos that they wish to have included on their photo page, create a folder
for each team and each player, and download the photos they submitted 
into their folder.
'''

import urllib.request as req
import os
import pandas as pd
import numpy as np


def open_excel_file(file_name):
    """ Open the excel file and put it into a pandas dataframe. """
    photo_df = pd.read_excel(file_name)
    return photo_df

def get_teams(data_frame):
    """Get the distinct team names from the file and create a directory for each one."""
    
    #Set the Team Names
    team_names = data_frame.Team.unique()
    
    return team_names

def create_team_directory(team):
    """create a directory for each team."""	
    try:
        print('Creating directory for {}\n'.format(team))
        os.mkdir(BASE_DIRECTORY+'/'+team)
    except:
        pass

def filter_team_data(team, data):
    """Create a data frame with just the data for a given team"""
    print('Creating dataframe for {}\n'.format(team))

    team_rows = data.loc[data['Team'] == team]

    return team_rows

def get_players(data_frame):
    """Get all the players for a given team."""
    print('Creating player data frame for {}\n'.format(team))
    player_list = team_data.Player_Name.unique()

    return player_list

def create_player_directory(team, players):
    """Create Directories for those players"""
    try:
        player_dir = str(team + '/' + str(player))
        print('Creating directory for {}.\n'.format(player))
        os.mkdir(BASE_DIRECTORY + '/' + player_dir)
    except:
        pass

def get_player_data(player, data):
    """Get the data for the specific player"""
    #get the pictures for each player
    player_data = data.loc[data['Player_Name'] == player].dropna(axis='columns')

    return player_data









def get_player_pictures(data):
    """Getting the pictures for the specifid player and putting them in their dirctory"""
    column_count = len(data.columns) - 2
    first_col = 1

    #list of photos for the player.
    url_list = []

    while first_col < column_count:
        col = 'Photo'+str(first_col)
        url_list.append(data[col].values[0])

        first_col += 1
        
    return url_list        




def download_photos(photo, pname):
    """ Download the player files and put them in his folder. """
    print('Downloading {} to {}\n'.format(photo, pname))
                
    req.urlretrieve(photo, pname)




##########
# Main Function
###########
if __name__ == '__main__':

    PLAYER_FILE = 'photolist.xlsx'

    #Open the file
    DF = open_excel_file(PLAYER_FILE)
    BASE_DIRECTORY = "/volumes/WD Elements/Pictures/DeSalesSoccer/2018/memorybook"
    
    #change to photos directory
    os.chdir(BASE_DIRECTORY)
    

    #get the list of team names and create a directory for each team.
    TEAM_DF = get_teams(DF)


    #Get all of the players on each team
    for team in TEAM_DF:
        print('Running for {}\n'.format(team))

        #Create the directories for the teams
        create_team_directory(team)

        #create data frame for each team
        team_data = filter_team_data(team, DF)

        #Get the Player List from each team.
        players = get_players(team_data)


        #Create Directories for each player
        for player in players:
            photo_count = 1
            #Create directory for the individual player
            create_player_directory(team, player)


            #get the photos for the player
            player_data = get_player_data(player, team_data)
            
            photo_list = get_player_pictures(player_data)

            #download pictures
            folder_name = team + '/' + player_data['Player_Name'].values[0] 

            os.chdir(BASE_DIRECTORY + '/' + folder_name)

            
            for photo in photo_list:
                photo_name = player_data['Player_Name'].values[0] + '_' + str(photo_count) + '.jpg'
                download_photos(photo, photo_name)
                photo_count += 1




