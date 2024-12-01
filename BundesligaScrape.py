import pandas as pd
from BundesligaStats import LeagueStats
class BundesligaScrape:
    def __init__(self):
        
        pass
    def assign_logo(self, data):
        # Create a dictionary mapping team names to logo paths
        logo_dict = {
            "Augsburg": r"BLogos\Augsburg.png",
            "Bayern Munich": r"BLogos\Bayern Munich.png",
            "Bochum": r"BLogos\Bochum.png",
            "Dortmund": r"BLogos\Dortmund.png",
            "Eint Frankfurt": r"BLogos\Eint Frankfurt.png",
            "Freiburg": r"BLogos\Freiburg.png",
            "Gladbach": r"BLogos\Gladbach.png",
            "Heidenheim": r"BLogos\Heidenheim.png",
            "Hoffenheim": r"BLogos\Hoffenheim.png",
            "Holstein Kiel": r"BLogos\Holstein Kiel.png",
            "Leverkusen": r"BLogos\Leverkusen.png",
            "Mainz 05": r"BLogos\Mainz 05.png",
            "RB Leipzig": r"BLogos\RB Leipzig.png",
            "St. Pauli": r"BLogos\St. Pauli.png",
            "Stuttgart": r"BLogos\Stuttgart.png",
            "Union Berlin": r"BLogos\Union Berlin.png", 
            "Werder Bremen": r"BLogos\Werder Bremen.png",
            "Wolfsburg": r"BLogos\Wolfsburg.png"
        }

        # Assign the correct logo path to each team
        data["LogoPaths"] = data["Squad"].map(logo_dict)
        return data
    def scrape(self):
        try:
            url = "https://fbref.com/en/comps/20/Bundesliga-Stats"
            table_id = "results2024-2025201_overall"
            df_list = pd.read_html(url, attrs={"id": table_id})
            
            if df_list:
                df = df_list[0]
                df=self.assign_logo(df)
                df.drop("Notes", axis=1, inplace=True)

                print(df.head())
                return df
                # Example usage of LeagueStats
                league_stats = LeagueStats(df)
                league_stats.highestXG()
            else:
                print(f"No tables found with id '{table_id}'")
        except Exception as e:
            print(f"An error occurred: {e}")