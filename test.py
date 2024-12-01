import BundesligaScrape
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import tkinter as tk
import numpy as np
import matplotlib.figure

class Gui:
    def __init__(self, df):
        self.df = df
        self.root = tk.Tk()
        self.root.geometry("1200x800")  # Set the size of the Tkinter window
        self.fig, self.ax = plt.subplots(figsize=(10, 6))  # Set the size of the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
   
    def getImage(self, path, zoom=1):
        return OffsetImage(plt.imread(path), zoom=zoom, alpha=0.9)
    
    def plotXG(self):
        self.ax.clear()
        y = self.df["xG"]
        x = self.df["GF"]
        
        x_max = max(x.max() + 5, y.max() + 5)
        self.ax.set_xlim(0, x_max)
        self.ax.set_ylim(0, x_max)

        # x coordinates for line
        line_x = np.linspace(0, x_max, 100)
        self.ax.scatter(x, y)
        
        self.ax.plot(line_x, line_x, color='red', linestyle='--', label='xG = GF')

        # shade regions
        self.ax.fill_betweenx(np.linspace(0, x_max, 100), line_x, x_max,
                              color='green', alpha=0.1, label='Over-performing (GF > xG)')
        self.ax.fill_betweenx(np.linspace(0, x_max, 100), 0, line_x,
                              color='red', alpha=0.1, label='Under-performing (GF < xG)')
        
        # set labels
        self.ax.set_xlabel("Goals Scored (GF)")
        self.ax.set_ylabel("Expected Goals (xG)")
        self.ax.set_title("Team Performance: Goals Scored vs Expected Goals")
        self.ax.legend(loc="upper left", frameon=True)

        # set images
        for x0, y0, img in zip(x, y, self.df["LogoPaths"]):
            ab = AnnotationBbox(self.getImage(img, zoom=0.065), (x0, y0), frameon=False)
            self.ax.add_artist(ab)
        
        # Draw the canvas
        self.canvas.draw()
    def plotXGLine(self):
        self.ax.clear()  # Clear the previous plot

        # Extract data
        teams = self.df["Squad"]
        xG = self.df["GA"]
        xGA = self.df["xGA"]

        # Set positions for the bars
        x = np.arange(len(teams))  # the label locations
        bar_width = 0.4  # Width of each bar

        # Plot the bars
        self.ax.bar(x - bar_width / 2, xG, width=bar_width, label='Goals Against (GA)', color='red', alpha=0.8)
        self.ax.bar(x + bar_width / 2, xGA, width=bar_width, label='Expected Goals Against (xGA)', color='blue', alpha=0.8)

        # Customizing the plot
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(teams, rotation=90, fontsize=10)
        self.ax.set_xlabel("Teams")
        self.ax.set_ylabel("Values")
        self.ax.set_title("Goals Against (GA) vs Expected Goals Against (xGA)")
        self.ax.legend(loc="upper left")

        # Adding grid
        self.ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Drawing the canvas
        self.canvas.draw()





    def display(self):
        self.root.title("Bundesliga Stats")

        # Tkinter Application
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        label = tk.Label(frame, text="Bundesliga Stats")
        label.config(font=("Arial", 32))
        label.pack()

        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar_frame = tk.Frame(frame)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        toolbar.pack(side=tk.LEFT, anchor="w")

        tk.Button(frame, text="Plot xG", command=self.plotXG).pack(pady=10)
        tk.Button(frame, text="Bar Graph", command=self.plotXGLine).pack(pady=10)
        tk.Button(frame, text="Quit", command=self.root.quit).pack(pady=10)

        self.root.mainloop()
