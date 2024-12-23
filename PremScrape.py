import pandas as pd
# from BundesligaStats import LeagueStats
class PremScrape:
    def __init__(self):
        pass
    def assign_values(self, data):
        # Create a dictionary mapping team names to logo paths
        logo_dict = {
            "Arsenal": r"Logos\PremLogos\Arsenal.png",
            "Aston Villa": r"Logos\PremLogos\Aston Villa.png",
            "Bournemouth": r"Logos\PremLogos\Bournemouth.png",
            "Brentford": r"Logos\PremLogos\Brentford.png",
            "Brighton": r"Logos\PremLogos\Brighton.png",
            "Chelsea": r"Logos\PremLogos\Chelsea.png",
            "Crystal Palace": r"Logos\PremLogos\Crystal Palace.png",
            "Everton": r"Logos\PremLogos\Everton.png",
            "Fulham": r"Logos\PremLogos\Fulham.png",
            "Ipswich Town": r"Logos\PremLogos\Ipswich Town.png",
            "Leicester City": r"Logos\PremLogos\Leicester City.png",
            "Liverpool": r"Logos\PremLogos\Liverpool.png",
            "Manchester City": r"Logos\PremLogos\Manchester City.png",
            "Manchester Utd": r"Logos\PremLogos\Manchester Utd.png",
            "Newcastle Utd": r"Logos\PremLogos\Newcastle Utd.png",
            "Nott'ham Forest": r"Logos\PremLogos\Nottingham Forest.png",
            "Tottenham": r"Logos\PremLogos\Tottenham.png",
            "Southampton": r"Logos\PremLogos\Southampton.png",
            "West Ham": r"Logos\PremLogos\West Ham.png",
            "Wolves": r"Logos\PremLogos\Wolves.png"
        }
        
        colors={
            "Arsenal": "#EF0107",
            "Aston Villa": "#95BFE5",
            "Bournemouth": "#DA291C",
            "Brentford": "#E30613",
            "Brighton": "#0057B8",
            "Chelsea": "#034694",
            "Crystal Palace": "#1B458F",
            "Everton": "#003399",
            "Fulham": "#CC0000",
            "Ipswich Town": "#0033A0",
            "Leicester City": "#003090",
            "Liverpool": "#C8102E",
            "Manchester City": "#6CABDD",
            "Manchester Utd": "#DA291C",
            "Newcastle Utd": "#241F20",
            "Nott'ham Forest": "#E53233",
            "Tottenham": "#132257",
            "Southampton": "#D71920",
            "West Ham": "#7A263A",
            "Wolves": "#FDB913",
           
        }

        data["Colors"] = data["Squad"].map(colors)
        data["LogoPaths"] = data["Squad"].map(logo_dict)
        #print(data["Colors"])
        #print(data["Squad"])
        return data
    
    def scrape(self):
        try:
            url = "https://fbref.com/en/comps/9/Premier-League-Stats"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            table_id = "results2024-202591_overall"
            #table_id2 = "all_stats_squads_standard"

            df_list = pd.read_html(url, attrs={"id": table_id})
            #print(df_list)
            #df_list2 = pd.read_html(url, attrs={"id": table_id2})
            #print(df_list2)

            print(df_list)
            if df_list :
                df = df_list[0]
                df = self.assign_values(df)
                df.drop("Notes", axis=1, inplace=True)
                
                #df1 = df_list2[0]
                #df1.columns = df1.columns.droplevel(0)

                #df = pd.merge(df, df1, on="Squad")
                #print(df.columns)
                #print(df)
                

                
                return df
            else:
                print(f"No tables found with ids '{table_id}' or '{table_id2}'")
                return None  # Explicitly return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
if __name__ == "__main__":
    scraper = PremScrape()
    df = scraper.scrape()
    if df is not None:
        print("Scraping successful. DataFrame head:")
        print(df)
    else:
        print("Scraping failed.")
