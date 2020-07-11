import requests 
from requests.exceptions import ConnectionError
import pprint
from bs4 import BeautifulSoup
import os
import tweepy

#global variables
base_url = 'https://na.leagueoflegends.com/en-us/news/game-updates/patch-'

def scrape(webpage):
    pp = pprint.PrettyPrinter(indent=4, compact=True)

    #URL = 'https://na.leagueoflegends.com/en-us/news/game-updates/patch-10-13-notes'
    page = requests.get(webpage)

    #create beautifulsoup object to parse HTML
    soup = BeautifulSoup(page.content, features = 'lxml')

    #find specific element by its ID
    results = soup.find(id='patch-notes-container')

    #find elements by HTML Class Name, creates an iterable
    patch_notes = results.find_all('div', class_='patch-change-block white-stone accent-before')

    for notes in patch_notes:
        #each note is a new BeautifulSoup object

        #locate change header, the name of champ/item being patched (lucian, hexdrinker, etc)
        change_header = notes.find('h3', class_='change-title')
        
        #locate summary (short summary of patch)
        summary = notes.find('p', class_="summary")

        #locate full summary (long description of patch)
        full_summary = notes.find('blockquote', class_="blockquote context")

        #locate change detail
        change_detail = notes.find_all('h4', class_="change-detail-title ability-title")

        #locate champion/item image
        reference_image = notes.find('img')

        #locate champion/item link
        reference_link = notes.find('a')['href']

        #check if either change header or summary has a 'None', in which case we should just continue to the next iterative
        if None in (change_header, summary):
            continue
            
        #print stuff we found
        print(reference_link)
        print (reference_image['src'])
        print(change_header.text.strip())
        print(summary.text.strip())
        print(full_summary.text.strip())
        print()

def page_exists(webpage):

    #get webpage
    page = requests.get(webpage)

    #create BS object out of webpage
    soup = BeautifulSoup(page.content, features = 'lxml')

    #locate main container for patch notes, basically we're checking to see if this page has content or it's just a '404' page
    request = soup.find(id='patch-notes-container')

    #if there's not any patch content, return False
    if (request is None):
        return False
    #found patch content, return True
    else:
        return True


def find_new_patch():
    #variables
    perform_patch_jump = False
    new_patches = []
    #set THIS_FOLDER to current absolute path
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

    #join together absolute path + file name
    patch_version_file = os.path.join(THIS_FOLDER, 'patch_versions.txt')

    #open up the file, print each line
    f = open(patch_version_file, "r")
    #print(f.readlines())

    #add all versions into a list, removing the newline character
    patch_versions = []
    line = f.readline()
    while line:
        line = line.strip()
        line = str(line)
        patch_versions.append(line)
        line = f.readline()
    f.close()

    #major patch = season version (10, 9, etc)
    major_patch = patch_versions[0][0:2]

    #check to see if there's a next patch version
    #first, obtain the latest patch (last patch in the text file)
    patch_version_to_check = patch_versions[-1]
    version = int(patch_versions[-1][3:])
    

    #loop until unable to find next patch version
    while (page_exists(base_url + patch_version_to_check + '-notes/') == True):
        if patch_version_to_check not in patch_versions:
            print ("New Patch: " + patch_version_to_check)
            new_patches.append(patch_version_to_check)
        #print("Found patch: " + patch_version_to_check)
        version = version + 1
        patch_version_to_check = major_patch + '-' + str(version)

    #LOGGING - NEW PATCHES
    print("No patch found for " + patch_version_to_check)
    print("All new patches found:\n")
    print(new_patches)

    #check for a major patch jump (ex. 10.14 - 11.1)
    '''major_patch_jump = int(major_patch)
    major_patch_jump = major_patch_jump + 1
    major_patch_jump = str(major_patch_jump)

    version_jump = 1
    patch_version_to_check_jump = major_patch_jump + '-1'
    while (page_exists(base_url + patch_version_to_check + '-notes/') == True):
        print("Found patch: " + patch_version_to_check)
        perform_patch_jump = True
        version_jump = version_jump + 1
        patch_version_to_check = major_patch_jump + '-' + str(version_jump)
    print("No patch found for " + patch_version_to_check_jump)

    #append current patch to file if not already in file'''
    
    

    #go back to most recent version found, scrap that page and print the results
    if (perform_patch_jump == False):
        #open up file, append current patch to file if not already in file
        f = open(patch_version_file, "a")
        for new_patch in new_patches:
            f.write('\n' + new_patch)
        f.close()

        #if there is a new patch, scrape the page, tweet about it
        if (len(new_patches) > 0):
            #set version back 1 since it overshoots during the patch check
            version = version - 1
            patch_version_to_check = major_patch + '-' + str(version)
            scrape(base_url + patch_version_to_check + '-notes/')

            #send tweet with new patch version
            compose_tweet(patch_version_to_check)
        else:
            print("No new patches")
    '''else:
        version_jump = version_jump - 1
        patch_version_to_check = major_patch_jump + '-' + str(version_jump)'''

    
def compose_tweet(patch_to_tweet):
    #set THIS_FOLDER to current absolute path
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    #join together absolute path + file name
    tkeys = os.path.join(THIS_FOLDER, 'tkeys.txt')

    #open up keys file, grab credentials for Twiter
    f = open(tkeys, "r")
    consumer_key = f.readline().strip()
    consumer_secret = f.readline().strip()
    token = f.readline().strip()
    token_secret = f.readline().strip()
    f.close()

    #add auth credentials
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(token, token_secret)

    api = tweepy.API(auth)

    '''public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)

    followers = api.followers()
    for follower in followers:
        print(follower.screen_name)'''

    api.update_status('!!! NEW PATCH !!!\n' + patch_to_tweet)

def main():
    print("Sweet")

    #run function to check for a new patch
    find_new_patch()

if __name__ == "__main__":

    main()
