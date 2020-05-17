from bs4 import BeautifulSoup
import requests


# -------------------------IMPORTANT INFO-------------------------------
#########################################################################################################

# GAMING PLATFORMS --------------------

# Battlefield V runs on 3 platforms, PS4, XBOX, and PC
# To search for player on a given platform, the 'platform' parameter in 'fetch_stats' functon must be: 
# PS4 = 'psn'
# XBOX = 'xbl'
# PC = 'origin'

# https://battlefieldtracker.com/bfv/profile/psn/Wonderbread200/overview
# https://battlefieldtracker.com/bfv/profile/origin/TaveracoTTV/overview
# https://battlefieldtracker.com/bfv/profile/xbl/Slothity/overview
# --------------------------------------------------------------------------


# FORMAT OF RETURN FROM def FETCH_STATS --------------------

# A players stats look like ....
# [('Score/min', '618.08'), ('K/D', '4.18'), ('Kills', '126043'), ('Kills/min', '1.52'), ('Wins', '2,999'), ('Deaths', '30188'), ('Assists', '26,258'), 
# ('Damage', '14,224,969'), ('Heals', '150,611'), ('Revives', '14473'), 
# ('Resupplies', '26,366')]

# Yes, as of now the commas are still there... 
# get rid of them if you like, I didn't b/c I didn't use that stat
# you can always add the stat if you like

# ----------------------------------------------------------------------------

#########################################################################################################


# --- Functions ---

def fetch_stats(platform,ID):
    """ Returns a list of tuples like (stat,value). Sends get request to BF Tracker.com and web scraps the stats and values  """


    # end product of 'sauce' for a sucessful get request
    # sauce = requests.get('https://battlefieldtracker.com/bfv/profile/psn/Wonderbread200/overview').text


    url = F'https://battlefieldtracker.com/bfv/profile/{platform}/{ID}/overview'


    sauce = requests.get(url).text

    #'lxml' is the parser
    soup = BeautifulSoup(sauce,'lxml')

    # the section of BF Tracker that is Scraped
    numbers = soup.find_all('div',class_='numbers')

    
    # going to hold a list of tuples of each (stat,value) for a given player
    stats = []


    # range starts at 4 b/c there is plenty of repettion of the kinds of stats, im not experienced with bs4...
    # and couldn't get the the second 'div' with the class of 'numbers' on BFV tracker, so this hacky move is my solution
    # the '-4' on the len(numbers) is skipping the data I think isn't important (Assult rank, Tanker spm, etc)
    for i in range(4,len(numbers)-4):

        # skipping win percentage, b/c its formatted like 'Win %'
        # ... I dont know how to handle that, tbh. 
        if i == 8:
            continue

        # kills, deaths, etc values are displayed with commas (43,232),
        # here is replacing the commas with nothing
        elif i == 6 or i == 10 or i == 14:
            title = numbers[i].text.split()[0]
            value = numbers[i].text.split()[1].replace(',',"")
            stats.append((title,value))
        else:
            # print(i,numbers[i].text)
            title = numbers[i].text.split()[0]
            value = numbers[i].text.split()[1]
            
            
            stats.append((title,value))
        

    return stats



def platoon_pass_in(ur_file,platform):
    """ Uses 'fetch_stats', takes in a txt file from the user, calculates stats and records them on another txt file """
    
    file_obj = open(ur_file)
    
    # Turns the content into a single string
    ur_file_content = file_obj.read()

    # a list that holds each platoon member's name in different indexes
    platoon_members = ur_file_content.splitlines()

    # 'Answer sheet', the stats will be recorded on another txt file
    platoon_stats = open('Stats.txt','w')



    #               --- Stats Calculated ---
    game_platform = platform    # Look at IMPORTANT INFO for more info
    spm_sum = 0                 # Score per Minute
    kd_sum = 0                  # Kill Death Ratio 
    kills_sum = 0               # Total Kills
    kills_min_sum = 0           # Kills per Minute
    deaths_sum = 0              # Total Deaths
    revives_sum = 0             # Total Revieves 
    ctr = 0                     # Counter to determine Averages




    for i in platoon_members:
        # print(i)
        try:
            # each BFV Platoon member is being ran, returning the list of tuples, (stat,value)
            player = fetch_stats(game_platform,i)

            ctr+=1
            # print(player)
            # print()

            # --- Summations ---
            spm_sum += float(player[0][1])
            kd_sum += float(player[1][1])
            kills_sum += int(player[2][1])
            kills_min_sum += float(player[3][1])
            deaths_sum += int(player[5][1])
            revives_sum += int(player[9][1])


        except:
            # may sometimes fail, and when it does, usualy all of it would, as the summations wont record
            # WHY? I'd guess b/c it was ran in the same time the stats on BF Tracker are updating
            print('Falied to get data for',i)
    



    #           --- Stats to txt file ---
    platoon_stats.write("Average SPM: {:.2f}".format(spm_sum/ctr))
    platoon_stats.write('\n')

    platoon_stats.write("Average K/D: {:.2f}".format(kd_sum/ctr))
    platoon_stats.write('\n')

    platoon_stats.write("Total Kills: " + str(kills_sum))
    platoon_stats.write('\n')

    platoon_stats.write("Average Kills: {:.2f}".format(kills_sum/ctr))
    platoon_stats.write('\n')

    platoon_stats.write("Average KPM: {:.2f}".format(kills_min_sum/ctr))
    platoon_stats.write('\n')

    platoon_stats.write("Total Deaths: " + str(deaths_sum))
    platoon_stats.write('\n')

    platoon_stats.write("Average Deaths: {:.2f}".format(deaths_sum/ctr))
    platoon_stats.write('\n')

    platoon_stats.write("Total Revives: " + str(revives_sum))
    platoon_stats.write('\n')

    platoon_stats.write("Average Revives: {:.2f}".format(revives_sum/ctr))
    platoon_stats.write('\n')


    file_obj.close()
    platoon_stats.close()

    # Could take a while to complete, so this msg is to notify when
    print('~STATS RECOREDED~')




# main ------------------
def main():

    platform = 'psn'
    platoon_roster = "TSC.txt"

    platoon_pass_in(platoon_roster,platform)


main()