import Scrape
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import numpy as np
import BundesligaStats
from BundesligaScrape import BundesligaScrape

def plot():
    bundesliga = BundesligaScrape.BundesligaScrape1()
    #bundesliga = bundesliga.assign_logo(bundesliga)
    #bundesliga.drop("Notes", axis=1, inplace=True)
    bundesliga_stats = BundesligaStats.LeagueStats(bundesliga.get_bundesliga_stats())
    bundesliga_stats.highestXG()
    print("hello")
    #bundesliga_stats.highestXGGraph()

    #Need to figure out how to display matplotlib graph in tkinter
    graph = bundesliga_stats.highestXGGraph()
    canvas.draw()
    

#intiizalize Tkinter
root = tk.Tk()
fig, ax = plt.subplots()

 

#Tkinter Application
frame = tk.Frame(root)
label = tk.Label(text="Bundesliga Stats")
label.config(font=("Arial", 32))
label.pack()


canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack()

frame.pack()

tk.Button(frame, text = "Overperforming and Underperforming Teams", command = plot).pack(pady=10)

root.mainloop()


