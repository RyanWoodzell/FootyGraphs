import pandas as pd
from BundesligaStats import LeagueStats
import numpy as np
class BundesligaScrape:
    def __init__(self):
        pass
    def assign_values(self, data):
        # Create a dictionary mapping team names to logo paths
        logo_dict = {
            "Augsburg": r"Logos\BLogos\Augsburg.png",
            "Bayern Munich": r"Logos\BLogos\Bayern Munich.png",
            "Bochum": r"Logos\BLogos\Bochum.png",
            "Dortmund": r"Logos\BLogos\Dortmund.png",
            "Eint Frankfurt": r"Logos\BLogos\Eint Frankfurt.png",
            "Freiburg": r"Logos\BLogos\Freiburg.png",
            "Gladbach": r"Logos\BLogos\Gladbach.png",
            "Heidenheim": r"Logos\BLogos\Heidenheim.png",
            "Hoffenheim": r"Logos\BLogos\Hoffenheim.png",
            "Holstein Kiel": r"Logos\BLogos\Holstein Kiel.png",
            "Leverkusen": r"Logos\BLogos\Leverkusen.png",
            "Mainz 05": r"Logos\BLogos\Mainz 05.png",
            "RB Leipzig": r"Logos\BLogos\RB Leipzig.png",
            "St. Pauli": r"Logos\BLogos\St. Pauli.png",
            "Stuttgart": r"Logos\BLogos\Stuttgart.png",
            "Union Berlin": r"Logos\BLogos\Union Berlin.png", 
            "Werder Bremen": r"Logos\BLogos\Werder Bremen.png",
            "Wolfsburg": r"Logos\BLogos\Wolfsburg.png"
            
        }
        #Map colors to each team
        colors={
            "Bayern Munich":"#dc052d",
            "Bochum": "#ADD8E6",
            "Dortmund": "#ffd900",
            "RB Leipzig": "#001f47",
            "Eint Frankfurt": "#E1000F",
            "Freiburg": "#FD1220",
            "Gladbach": "#808080",
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
      
        return data
    
    def scrape(self):
        try:
            url = "https://fbref.com/en/comps/20/Bundesliga-Stats"
            
            df_list = pd.read_html(url, attrs={"id": table_id} )
            df_list2 = pd.read_html(url, attrs={"id": table_id2})
            table_id = "results2024-2025201_overall"
            table_id2 = "stats_squads_standard_for"

            df_list = pd.read_html(url, attrs={"id": table_id})
            df_list2 = pd.read_html(url, attrs={"id": table_id2})
            
            
            
            
            if df_list and df_list2: # Check if tables were found
                df = df_list
                df = self.assign_values(df)
                df.drop("Notes", axis=1, inplace=True)
                
                df1 = df_list2[0]
                df1.columns = df1.columns.droplevel(0)

                df = pd.merge(df, df1, on="Squad")
                
                return df
            else:
                print(f"No tables found with ids '{table_id}' or '{table_id2}'")
                return None, None  # Explicitly return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None
        
    #Test Function for Github pictures
    def test(self):
        squads = {
                "Bayern Munich": "#dc052d",
                "Bochum": "#ADD8E6",
                "Dortmund": "#ffd900",
                "RB Leipzig": "#001f47",
                "Eint Frankfurt": "#E1000F",
                "Freiburg": "#FD1220",
                "Gladbach": "#000000",
                "Heidenheim": "#e2001a",
                "Hoffenheim": "#1961B5",
                "Holstein Kiel": "#0F5787",
                "Leverkusen": "#E32221",
                "Mainz 05": "#C3141E",
                "St. Pauli": "#624839",
                "Stuttgart": "#E32219",
                "Union Berlin": "#EB1923",
                "Werder Bremen": "#009655",
                "Augsburg": "#ba3733",
                "Wolfsburg": "#52a600"
            }
        data =  {
                "Squad": list(squads.keys()),
                "xG": np.random.rand(len(squads)) * 50,
                "GF": np.random.rand(len(squads)) * 50,
                "xGA": np.random.rand(len(squads)) * 50,
                "GA": np.random.rand(len(squads)) * 50,
                "Attendance": np.random.randint(20000, 50000, size=len(squads)),
            }
        df_list = pd.DataFrame(data)
        df_list = self.assign_values(df_list)
        return df_list