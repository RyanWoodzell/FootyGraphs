import pandas as pd
from BundesligaScrape import BundesligaScrape
from test import Gui

class League:
    def __init__(self, name):
        if name.lower() not in ["bundesliga", "premier league", "la liga", "serie a", "ligue 1", "champions league"]:
            raise ValueError("Invalid league name. Please choose from 'Bundesliga', 'Premier League', 'La Liga', 'Serie A', or 'Ligue 1'")
        self.df = None
        self.df2 = None
        
        if name.lower() == "bundesliga":
            self.name = name
            scraper = BundesligaScrape()
            self.df = scraper.scrape()

            #print(self.df.head())
            #blgui = Gui(self.df)
            #blgui.displayTest()
            

        if name.lower() == "premier league":
            pass
        if name.lower() == "la liga":
            pass
        if name.lower() == "serie a":
            pass
        if name.lower() == "ligue 1":
            pass
        self.teams = []

    def getdf(self):
        return self.df
    #print the league name
    def __str__(self):
        return self.name

def main():
    league = League("bundesliga")
    
    #print(league)

if __name__ == "__main__":
    main()