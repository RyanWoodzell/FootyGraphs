from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import tkinter as tk
import numpy as np
import pandas as pd

class Gui:
    def __init__(self, df, league):

        self.df = df
        self.league = league
        self.root = tk.Tk()
        self.root.geometry("1200x800")
        
        # Set up main frame for the content
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        #set up title at top of window
        if self.league == "bundesliga":
            self.title_label = tk.Label(self.main_frame, text="Bundesliga Stats", font=("Helvetica", 24, "bold"))
        elif self.league == "premier league":
            self.title_label = tk.Label(self.main_frame, text="Premier League Stats", font=("Helvetica", 24, "bold"))
        self.title_label.pack(side=tk.TOP, pady=20)
        
        # Create and pack buttons below the title
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        
        tk.Button(self.button_frame, text="Plot Expected Goals Vs. Actual Goals", command=self.plotXG).pack(padx=10)
        tk.Button(self.button_frame, text="Plot Expected Goals Against Vs. Actual Goals Against", command=self.plotGaVSxGA).pack(padx=10)
        tk.Button(self.button_frame, text="View Attendance", command=self.plotAttendanceHeatmap).pack(padx=10)
        tk.Button(self.button_frame, text="Goals Pie Chart", command=self.goalsPie).pack(padx=10)
        
        
        # Create Matplotlib figure and axis
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Necessary to remove colorbar after initializations
        self.colorbar = None
        
        self.root.mainloop()

    def clearCanvas(self):
    # Clear the existing canvas if it exists
        if self.canvas.get_tk_widget():
            self.canvas.get_tk_widget().destroy()

        # Recreate canvas
        self.fig, self.ax = plt.subplots(figsize=(10, 6))  # Set the size of the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def getImage(self, path, zoom=1):
        return OffsetImage(plt.imread(path), zoom=zoom, alpha=0.9)
    
    def plotXG(self):
        self.clearCanvas()  # Clear the current canvas

        if self.colorbar:
            self.colorbar.remove()  # Remove the color bar if it exists
            self.colorbar = None  # Reset the color bar reference

        # Extract data. For some reason bundesliga uses xG_x and premier league uses xG
        if self.league == "bundesliga":
            y = self.df["xG_x"]
        elif self.league == "premier league":
            y = self.df["xG"]

        #y = self.df["xG"]. USed for test df
        x = self.df["GF"]
        
        # Set limits for the plot
        x_max = max(x.max() + 5, y.max() + 5)
        self.ax.set_xlim(0, x_max)
        self.ax.set_ylim(0, x_max)

        # x coordinates for line
        line_x = np.linspace(0, x_max, 100)
        self.ax.scatter(x, y)
        
        # plot line x=y. Line that seperates overperforming and underperforming teams
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

    def plotGaVSxGA(self):
        
        self.clearCanvas()  # Clear the current canvas

        if self.colorbar:
            self.colorbar.remove()  # Remove the color bar if it exists
            self.colorbar = None  # Reset the color bar reference

        # Extract data
        teams = self.df["Squad"]
        xG = self.df["GA"]
        xGA = self.df["xGA"]
        logo_paths = self.df["LogoPaths"] 

        # Set positions for the bars
        x = np.arange(len(teams))  # the label locations
        bar_width = 0.4  # Width of each bar

        # Plot the bars
        self.ax.bar(x - bar_width / 2, xG, width=bar_width, label='Goals Against (GA)', color='red', alpha=0.8)
        self.ax.bar(x + bar_width / 2, xGA, width=bar_width, label='Expected Goals Against (xGA)', color='blue', alpha=0.8)

        # Set labels and title
        self.ax.set_ylabel("Values")
        self.ax.set_title("Goals Against (GA) vs Expected Goals Against (xGA)")
        self.ax.legend(loc="upper left")

        # Replace text tick labels with images
        self.ax.set_xticks(x)  # Set tick positions
        self.ax.set_xticklabels([])  # Remove default tick labels

        # Add team logos as tick labels
        for idx, (x_pos, logo_path) in enumerate(zip(x, logo_paths)):
            image = self.getImage(logo_path, zoom=0.065)  # Load the logo image
            ab = AnnotationBbox(image, (x_pos, 1),  # Position below the bars
                                frameon=False, box_alignment=(0.5, 0.5))
            self.ax.add_artist(ab)

        # Adjust the limits to fit logos
        self.ax.set_xlim(-1, len(teams))
        self.ax.set_ylim(0, max(max(xG), max(xGA)) * 1.2)  # Add some padding above the bars

        # Adding grid
        self.ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Drawing the canvas
        self.canvas.draw()

    def goalsPie(self):
        self.clearCanvas()  # Clear the current canvas

        # Plot the pie chart
        wedges, texts, autotexts = self.ax.pie(self.df["GF"], labels=self.df["Squad"], colors=self.df["Colors"], autopct='%1.1f%%', startangle=90)
        self.ax.set_title("Goals Scored by Team")

        # Add logos to the pie chart
        for wedge, logo_path in zip(wedges, self.df["LogoPaths"]):
            angle = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
            x = np.cos(np.radians(angle))
            y = np.sin(np.radians(angle))
            image = self.getImage(logo_path, zoom=0.05)
            ab = AnnotationBbox(image, (x, y), frameon=False, box_alignment=(0.5, 0.5), xycoords='data', pad=0.1)
            self.ax.add_artist(ab)

        self.canvas.draw()
       
    
    def plotAttendanceHeatmap(self):
        # Clear previous plot
        self.clearCanvas()  # Clear the current canvas

        if self.colorbar:
            self.colorbar.remove()
            self.colorbar = None

        # Extract attendance data and team information
        teams = self.df["Squad"]
        attendance = self.df["Attendance"].values.reshape(1, -1)  # Reshape for heatmap
        logo_paths = self.df["LogoPaths"]  # Paths to team logos

        # Create the heatmap
        heatmap = self.ax.imshow(attendance, cmap='YlOrRd', aspect='auto')

        # Add a new colorbar and store its reference
        self.colorbar = self.fig.colorbar(heatmap, ax=self.ax, orientation='vertical', pad=0.02)
        self.colorbar.set_label("Attendance", rotation=270, labelpad=15)

        # Customize axes
        self.ax.set_xticks(np.arange(len(teams)))  # Tick positions
        self.ax.set_yticks([])  # No y-axis ticks
        self.ax.set_xticklabels([])  # Remove default x-axis labels

        # Replace x-axis ticks with team logos
        for idx, (x_pos, logo_path) in enumerate(zip(np.arange(len(teams)), logo_paths)):
            image = self.getImage(logo_path, zoom=0.065)
            ab = AnnotationBbox(image, (x_pos, 0), frameon=False, box_alignment=(0.5, -0.1))
            self.ax.add_artist(ab)

        # Adjust layout and redraw canvas
        #self.fig.tight_layout()
        self.canvas.draw()

   