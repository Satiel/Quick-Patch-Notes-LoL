import requests 
from requests.exceptions import ConnectionError
import pprint
from bs4 import BeautifulSoup
import os

def scrape(webpage):
    pp = pprint.PrettyPrinter(indent=4, compact=True)

    #URL = 'https://na.leagueoflegends.com/en-us/news/game-updates/patch-10-13-notes'
    page = requests.get(webpage)

    #create beautifulsoup object to parse HTML
    soup = BeautifulSoup(page.content, features = 'lxml')

    #find specific element by its ID
    results = soup.find(id='patch-notes-container')

    #find elements by HTML Class Name, creates an iterable
    #patch_notes = results.find_all('section', class_='card-content')
    patch_notes = results.find_all('div', class_='patch-change-block white-stone accent-before')
    #find only specific job
    #python_jobs = results.find_all('h2', string='Python Developer')
    # function version
    '''
    python_jobs = results.find_all('h2',
                                    string=lambda text: 'python' in text.lower())

    analyst_jobs = results.find_all('h2', 
                                    string=lambda text: 'analyst' in text.lower())
    '''

    #loop through class names
    #for job_elem in job_elems:
      # each job_elem is a new BeautifulSoup object.
        # You can use the same methods on it as you did before
        #title_elem = job_elem.find('h2', class_='title')
        #company_elem = job_elem.find('div', class_='company')
        #location_elem = job_elem.find('div', class_='location')
     #if None in (title_elem, company_elem, location_elem):
        #continue
    #print(title_elem.text.strip())
    #print(company_elem.text.strip())
    #print(location_elem.text.strip())
    #print()

    #print(len(python_jobs))

    #loop through class names

    for notes in patch_notes:
        #each note is a new BeautifulSoup object
        change_header = notes.find('h3', class_='change-title')
        summary = notes.find('p', class_="summary")
        full_summary = notes.find('blockquote', class_="blockquote context")
        change_detail = notes.find_all('h4', class_="change-detail-title ability-title")
        #attribute_change = notes.find_all('div', class_="attribute-change")
        reference_image = notes.find('img')
        reference_link = notes.find('a')['href']


        #change_title = notes.find('h3', class_='change-title')
        #change_title_object = change_title.find('a')['href']
        if None in (change_header, summary):
            continue
        #change_title - notes.find('a')['href']
        #link = notes.find('a')['href']
        print(reference_link)
        print (reference_image['src'])
        print(change_header.text.strip())
        print(summary.text.strip())
        print(full_summary.text.strip())
        #for change in change_detail:
            #print(change.text.strip())

        print()
    

    
#print(patch_notes)
'''
for p_job in python_jobs:
    link = p_job.find('a')['href']
    print(p_job.text.strip())
    print(f"Apply here: {link}\n")

    #print(job_elem, end='\n'*2)
for p_job in analyst_jobs:
    link = p_job.find('a')['href']
    print(p_job.text.strip())
    print(f"Apply here: {link}\n")

#pp.pprint(page.content)
#print(results.prettify())

'''

def page_exists(webpage):
    page = requests.get(webpage)
    soup = BeautifulSoup(page.content, features = 'lxml')
    request = soup.find(id='patch-notes-container')
    #print(request)
    if (request is None):
        return False
    else:
        return True
    
    '''
    request = requests.get('https://na.leagueoflegends.com/en-us/news/game-updates/patch-10-13-notes/')
    except ConnectionError:
        print("Website does not exist")
    else:
        print("Web site exists")
    print(request.status_code)
    print(request.text)'''

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

    #peek into last version on the list

    print(patch_versions[0])
    print(patch_versions[0][0:2])

    patch_version_to_check = patch_versions[0][0:2] + '-1'
    version = 1
    while (page_exists('https://na.leagueoflegends.com/en-us/news/game-updates/patch-' + patch_version_to_check + '-notes/') == True):
        print("Found patch: " + patch_version_to_check)
        version = version + 1
        patch_version_to_check = patch_versions[0][0:2] + '-' + str(version)
    print("No patch found for " + patch_version_to_check)

    version = version - 1
    patch_version_to_check = patch_versions[0][0:2] + '-' + str(version)
    scrape('https://na.leagueoflegends.com/en-us/news/game-updates/patch-' + patch_version_to_check + '-notes/')
        

    '''if page_exists('https://na.leagueoflegends.com/en-us/news/game-updates/patch-' + str(version_plus_10) + '-notes/') == True:
        print ("Found patch: " + version_plus_10)
    elif page_exists('https://na.leagueoflegends.com/en-us/news/game-updates/patch-' + str(version_plus_01) + '-notes/') == True:
        print("Found patch: " + version_plus_01)
    else:
        print ("No new patch found after " + patch_versions[-1])'''


    

if __name__ == "__main__":
    print("Sweet")
    '''new_patch_page = 'https://na.leagueoflegends.com/en-us/news/game-updates/patch-10-13-notes/'
    #scrape()
    if page_exists(new_patch_page) == True:
        scrape(new_patch_page)
    else:
        print("Page not found")'''

    find_new_patch()