import BundesligaScrape

class Scraper:
    def __init__(self, league):
        if league.lower() not in ["bundesliga", "premier league", "la liga", "serie a", "ligue 1"]:
            raise ValueError("Invalid league name. Please choose from 'Bundesliga', 'Premier League', 'La Liga', 'Serie A', or 'Ligue 1'")
        
        if league.lower() == "bundesliga":
            BundesligaScrape.BundesligaScrape()

        if league.lower() == "premier league":
            pass
        if league.lower() == "la liga":
            pass
        if league.lower() == "serie a":
            pass
        if league.lower() == "ligue 1":
            pass
        
        self.league = league
        self.df = None

    
