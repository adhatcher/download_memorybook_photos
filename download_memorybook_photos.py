#download_memorybook_photos.py
'''
This will import a spreadsheet from a google form with a list of players
and photos that they wish to have included on their photo page, create a folder
for each team and each player, and download the photos they submitted 
into their folder.
'''

import password as pwd
import download_functions as dlf
from download_functions import logging
import urllib.request as req
import os
import logging
##########
# Main Function
###########
if __name__ == '__main__':



    log = logging.getLogger(__name__)

    logging.basicConfig(level=logging.INFO)
    
    api_key = pwd.get_api()
    URL_BASE = "https://api.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key=" \
    + api_key  + "&format=json&nojsoncallback=1" \
    + "&photo_id="
    

    PLAYER_FILE = 'photolist.xlsx'

    #Open the file
    DF = dlf.open_excel_file(PLAYER_FILE)
    BASE_DIRECTORY = "/volumes/WD Elements/Pictures/memorybook"
    
    #change to photos directory
    os.chdir(BASE_DIRECTORY)
    

    #get the list of team names and create a directory for each team.
    TEAM_DF = dlf.get_teams(DF)


    #Get all of the players on each team
    for team in TEAM_DF:
        print('Running for {}\n'.format(team))

        
        if os.path.isdir(BASE_DIRECTORY + '/' + team):
            pass
        else:
            #Create the directories for the teams
            dlf.create_team_directory(team, BASE_DIRECTORY)

        #create data frame for each team
        team_data = dlf.filter_team_data(team, DF)

        #Get the Player List from each team.
        players = dlf.get_players(team_data, team)


        #Create Directories for each player
        for player in players:
            photo_count = 1
            
            #if the folder exists, skip it and move on to the next player
           
            if os.path.isdir(BASE_DIRECTORY + '/' + team + '/' + player):
                log.info('Skipping {}.'.format(player))
                pass
            else:
                #Create directory for the individual player
                dlf.create_player_directory(team, player, BASE_DIRECTORY)

                #get the photos for the player
                player_data = dlf.get_player_data(player, team_data)
                
                photo_list = dlf.get_player_picture_data(player_data)

                #download pictures
                folder_name = team + '/' + player_data['Player_Name'].values[0] 
                    
                os.chdir(BASE_DIRECTORY + '/' + folder_name)
                
                for photo in photo_list:
                    photo_name = player_data['Player_Name'].values[0] + '_' + \
                                str(photo_count) + '.jpg'
                    #Check to see if the url is an actual JPG file, or flicker page.
                    if photo.endswith('.jpg'):
                        log.info('Downloading jpg for {}'.format(player_data['Player_Name'].values[0]))
                        req.urlretrieve(photo, photo_name)
                        photo_count += 1
                    else:
                        dlf.download_photos(URL_BASE, photo, photo_name)
                        photo_count += 1
