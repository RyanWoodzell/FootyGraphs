import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

class LeagueStats:
    def __init__(self, data):
        self.data = data
    

    def getImage(self, path, zoom=1):
        return OffsetImage(plt.imread(path), zoom=zoom, alpha=0.9)
    
    def highestXG(self):
        #sort data by xG
        topXG = self.data.sort_values(by="xG", ascending=False)
        topXG = topXG[["Rk", "Squad", "xG", "GF", "LogoPaths"]]
        topXG = topXG.reset_index(drop=True)
        topXG.index += 1
        print(topXG)

    def highestXGGraph(self):

        #create scatter plot
        fig, ax = plt.subplots()

        #sort data by xG
        topXG = self.data.sort_values(by="xG", ascending=False)
        topXG = topXG[["Rk", "Squad", "xG", "GF", "LogoPaths"]]
        topXG = topXG.reset_index(drop=True)
        topXG.index += 1
        #print(topXG)
        
        #establish x and y points
        ypoints = topXG["xG"]
        xpoints = topXG["GF"]

        #establish max value for x and y to divide graph into halves
        x_max = max(xpoints.max()+5, ypoints.max()+5)
        ax.set_xlim(0, x_max)
        ax.set_ylim(0, x_max)

        #x coordinates for line
        x=np.linspace(0, x_max, 100)
        
        #create scatter plot
        ax.scatter(xpoints, ypoints)
        ax.plot(x, x, color='red', linestyle='--', label='xG = GF')

        #shade regions
        ax.fill_betweenx(np.linspace(0, x_max, 100), x, x_max,
                 color='green', alpha=0.1, label='Over-performing (GF > xG)')
        ax.fill_betweenx(np.linspace(0, x_max, 100), 0, x,
                 color='red', alpha=0.1, label='Under-performing (GF < xG)')
        
        #set labels
        ax.set_ylabel("Expected Goals (xG)")
        ax.set_xlabel("Goals Scored (GF)")
        ax.set_title("Team Performance: Goals Scored vs Expected Goals")
        ax.legend(loc="upper left", frameon=True)
        
        #assign logos to each specific point
        for x0, y0, img in zip(xpoints, ypoints, topXG["LogoPaths"]):
            ab = AnnotationBbox(self.getImage(img, zoom=0.065), (x0, y0), frameon=False)
            plt.gca().add_artist(ab)
        
        return plt
        #show plot
        #plt.show()
    

