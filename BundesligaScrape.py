import pandas as pd
from BundesligaStats import LeagueStats
class BundesligaScrape:
    def __init__(self):
        pass
    def assign_values(self, data):
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
        
        colors={
            "Bayern Munich":"#dc052d",
            "Bochum": "#ADD8E6",
            "Dortmund": "#ffd900",
            "RB Leipzig": "#001f47",
            "Eint Frankfurt": "#E1000F",
            "Freiburg": "#FD1220",
            "Gladbach": "#000000",
            "Heidenheim":"#e2001a",
            "Hoffenheim": "#1961B5",
            "Holstein Kiel": "#0F5787",
            "Leverkusen": "#E32221",
            "Mainz 05": "#C3141E",
            "RB Leipzig": "#DD0741",
            "St. Pauli": "#624839",
            "Stuttgart": "#E32219",
            "Union Berlin": "#EB1923",
            "Werder Bremen": "#009655",
            "Augsburg": "#ba3733",
            "Wolfsburg": "#52a600",
        }

        data["Colors"] = data["Squad"].map(colors)
        data["LogoPaths"] = data["Squad"].map(logo_dict)
        #print(data["Colors"])
        #print(data["Squad"])
        return data
    
    def scrape(self):
        try:
            url = "https://fbref.com/en/comps/20/Bundesliga-Stats"
            table_id = "results2024-2025201_overall"
            table_id2 = "stats_squads_standard_for"

            df_list = pd.read_html(url, attrs={"id": table_id})
            df_list2 = pd.read_html(url, attrs={"id": table_id2})

            if df_list and df_list2:
                df = df_list[0]
                df = self.assign_values(df)
                df.drop("Notes", axis=1, inplace=True)
                
                df1 = df_list2[0]
                df1.columns = df1.columns.droplevel(0)

                df = pd.merge(df, df1, on="Squad")
                print(df.head())
                

                
                return df
            else:
                print(f"No tables found with ids '{table_id}' or '{table_id2}'")
                return None, None  # Explicitly return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None