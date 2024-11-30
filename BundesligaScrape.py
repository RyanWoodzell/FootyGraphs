import pandas as pd
from BundesligaStats import LeagueStats

try:
    url = "https://fbref.com/en/comps/20/Bundesliga-Stats"
    table_id = "results2024-2025201_overall"
    df_list = pd.read_html(url, attrs={"id": table_id})
    
    if df_list:
        df = df_list[0]
        print(df.head())
        topXG = df.sort_values(by="xG", ascending=False).head(10)
        bsStats = LeagueStats(df)
        bsStats.highestXG()
        #predictor = Prediction(df) # Create an instance of the Prediction class
        #predictor.predict()
    else:
        print(f"No tables found with id '{table_id}'")
except Exception as e:
    print(f"An error occurred: {e}")