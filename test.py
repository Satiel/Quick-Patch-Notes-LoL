from patchnotes_scrape import scrape

def main():
    
    print("Sweet")

    #run function to check for a new patch
    scrape('https://na.leagueoflegends.com/en-us/news/game-updates/patch-10-14-notes/')

if __name__ == "__main__":

    main()
