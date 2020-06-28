import requests 
import pprint
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4, compact=True)

URL = 'https://na.leagueoflegends.com/en-us/news/game-updates/patch-10-13-notes'
page = requests.get(URL)

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