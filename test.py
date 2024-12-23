from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
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
        self.title_label = tk.Label(self.main_frame, text="Bundesliga Stats", font=("Helvetica", 24, "bold"))
        self.title_label.pack(side=tk.TOP, pady=20)
        
        # Create and pack buttons below the title
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        
        tk.Button(self.button_frame, text="Plot xG", command=self.plotXG).pack(padx=10)
        tk.Button(self.button_frame, text="Plot xG Line", command=self.plotGaVSxGA).pack(padx=10)
        tk.Button(self.button_frame, text="Plot Attendance Heatmap", command=self.plotAttendanceHeatmap).pack(padx=10)
        tk.Button(self.button_frame, text="Pie", command=self.goalsPie).pack(padx=10)
        
        
        # Create Matplotlib figure and axis
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        '''
        toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        toolbar.pack()
        '''
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
        #self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    def getImage(self, path, zoom=1):
        return OffsetImage(plt.imread(path), zoom=zoom, alpha=0.9)
    
    def plotXG(self):
        self.clearCanvas()  # Clear the current canvas

        if self.colorbar:
            self.colorbar.remove()  # Remove the color bar if it exists
            self.colorbar = None  # Reset the color bar reference
        if self.league == "bundesliga":
            y = self.df["xG_x"]
        elif self.league == "premier league":
            y = self.df["xG"]
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

    def plotGaVSxGA(self):
        
        self.clearCanvas()  # Clear the current canvas

        if self.colorbar:
            self.colorbar.remove()  # Remove the color bar if it exists
            self.colorbar = None  # Reset the color bar reference

        # Extract data
        teams = self.df["Squad"]
        xG = self.df["GA"]
        xGA = self.df["xGA"]
        logo_paths = self.df["LogoPaths"]  # Assume this column contains paths to the logo images

        # Set positions for the bars
        x = np.arange(len(teams))  # the label locations
        bar_width = 0.4  # Width of each bar

        # Plot the bars
        self.ax.bar(x - bar_width / 2, xG, width=bar_width, label='Goals Against (GA)', color='red', alpha=0.8)
        self.ax.bar(x + bar_width / 2, xGA, width=bar_width, label='Expected Goals Against (xGA)', color='blue', alpha=0.8)

        # Set labels and title
        self.ax.set_ylabel("Values")
        self.ax.set_title("Expected Goals (xG) vs Expected Goals Against (xGA)")
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
    '''
    def plotDefenseVsOffenseRadar(self, teams_to_compare=None):
        self.ax.clear()
        if self.colorbar:
            self.colorbar.remove()
            self.colorbar = None

        # Define metrics for radar chart
        metrics = ["GF", "xG", "GA", "xGA"]
        
       # Normalize data for radar chart
        df_normalized = self.df.copy()
        for metric in metrics:
            df_normalized[metric] = (self.df[metric] - self.df[metric].min()) / (self.df[metric].max() - self.df[metric].min())

        # Teams to compare
        if teams_to_compare is None:
            teams_to_compare = ["Team1", "Team2"]  # Default comparison (replace with actual team names)

        # Number of variables
        num_vars = len(metrics)

        # Compute angle for each axis
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]  # Complete the loop
# Initialize radar chart
        self.ax = plt.subplot(111, polar=True)

        # Plot each team
        for team in teams_to_compare:
            values = df_normalized.loc[self.df["Squad"] == team, metrics].values.flatten().tolist()
            values += values[:1]  # Complete the loop
            self.ax.plot(angles, values, label=team)
            self.ax.fill(angles, values, alpha=0.25)

        # Add labels
        self.ax.set_yticklabels([])
        self.ax.set_xticks(angles[:-1])
        self.ax.set_xticklabels(metrics)

        # Add title and legend
        self.ax.set_title("Defense vs Offense Radar Chart")
        self.ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))

        # Draw the canvas
        self.canvas.draw()
        '''
    '''
    def display(self):
        self.root.title("Bundesliga Stats")

        # Tkinter Application
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        label = tk.Label(frame, text="Bundesliga Stats")
        label.config(font=("Arial", 32))
        label.pack()
        #label.grid(row=0, column=0, pady=20)

        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar_frame = tk.Frame(frame)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        toolbar.pack(side=tk.LEFT, anchor="w")

        tk.Button(frame, text="Plot xG", command=self.plotXG).pack(pady=10)
        tk.Button(frame, text="Plot xG Line", command=self.plotXGLine).pack(pady=10)
        tk.Button(frame, text="Plot Attendance Heatmap", command=self.plotAttendanceHeatmap).pack(pady=10)
        #tk.Button(frame, text="Plot Defense vs Offense Radar", command=self.plotDefenseVsOffenseRadar).pack(pady=10)
        tk.Button(frame, text="Pie", command=self.goalsPie).pack(pady=10)

        self.root.mainloop() 

    def displayTest(self):
        self.root.title("Bundesliga Stats")
        
        # Create a main frame for the content
        main_frame = tk.Frame(self.root)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Label at the top
        label = tk.Label(main_frame, text="Bundesliga Stats")
        label.config(font=("Arial", 32))
        label.grid(row=0, column=0, pady=20)

        # Canvas for the plot
        self.canvas.get_tk_widget().grid(row=1, column=0, pady=20)

        # Frame for the buttons
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10)
        
        # Adding buttons
        tk.Button(button_frame, text="Plot xG", command=self.plotXG).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Plot xG Line", command=self.plotXGLine).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Plot Attendance Heatmap", command=self.plotAttendanceHeatmap).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="Pie", command=self.goalsPie).grid(row=0, column=3, padx=10)

        self.root.mainloop()
        '''