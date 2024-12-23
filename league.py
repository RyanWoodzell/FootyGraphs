import pandas as pd
from BundesligaScrape import BundesligaScrape
from PremScrape import PremScrape
from GraphInitalizer import Gui

class League:
    def __init__(self, name):
        # Exception Handling
        if name.lower() not in ["bundesliga", "premier league", "la liga", "serie a", "ligue 1", "champions league"]:
            raise ValueError("Invalid league name. Please choose from 'Bundesliga', 'Premier League', 'La Liga', 'Serie A', or 'Ligue 1'")
        self.df = None
        self.df2 = None
        
        if name.lower() == "bundesliga":

            self.name = name

            #Scrape the data
            scraper = BundesligaScrape()
            self.df = scraper.test()
            
            #Display the data
            blgui = Gui(self.df, self.name)
            blgui.displayTest()
            

        if name.lower() == "premier league":
            self.name = name

            #Scrape the data
            scraper = PremScrape()
            self.df = scraper.scrape()

            #Display the data
            blgui = Gui(self.df, 'Premier League')
            blgui.displayTest()
            
        if name.lower() == "la liga":
            pass
        if name.lower() == "serie a":
            pass
        if name.lower() == "ligue 1":
            pass
        self.teams = []

    #Getter methods for testing
    def getdf(self):
        return self.df
    #print the league name
    def __str__(self):
        return self.name

def main():
    league = League("Bundesliga")
    #league = League("Premier League")
    
if __name__ == "__main__":
    main()