import requests 
from requests.exceptions import ConnectionError
import pprint
from bs4 import BeautifulSoup
import os

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
    patch_version_to_check = major_patch + '-1'
    version = 1

    #loop until unable to find next patch version
    while (page_exists(base_url + patch_version_to_check + '-notes/') == True):
        print("Found patch: " + patch_version_to_check)
        version = version + 1
        patch_version_to_check = major_patch + '-' + str(version)
    print("No patch found for " + patch_version_to_check)

    #go back to most recent version found, scrap that page and print the results
    version = version - 1
    patch_version_to_check = major_patch + '-' + str(version)
    scrape(base_url + patch_version_to_check + '-notes/')

if __name__ == "__main__":
    print("Sweet")
    
    #run function to check for a new patch
    find_new_patch()