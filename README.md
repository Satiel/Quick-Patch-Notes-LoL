# Quick and Dirty LoL Patch Notes
<img src="https://img.shields.io/travis/satiel/Quick-Patch-Notes-LoL">

 **A simplified version of the League of Legends patch notes, obtained via webscraping and pushed to Twitter.**
 
 
This script is designed to keep an eye on the League of Legends patch notes website, constantly looking for any new patch notes uploads. If there is a new patch notes page, it will be scraped for the most important pieces of information, including: 
- **Champion / Item Names** (*ex. Varus, Azir, Death's Dance*)
- **Patch Summary** (*ex. "E cost increased"8)
- **Full Patch Summary** (*flavor text from the devs*)
- **Detailed Attribute Changes** (*ex. Attack Damage Growth 2.2 ⇒ 2*)

Posts a tweet to a dedicated Twitter account, adding a link to the scraped version of the patch notes page.

# Task List

- [x] Develop code for parsing the patch notes webpage for information
- [x] Check for newly uploaded patch notes webpage
- [ ] Tweet when new patch notes webpage is located
- [ ] Automatically parse new patch notes webpage
- [ ] Tweet upon successful completion of parse
