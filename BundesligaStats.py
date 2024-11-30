import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

class LeagueStats:
    def __init__(self, data):
        self.data = data

    def getImage(self, path, zoom=1):
        return OffsetImage(plt.imread(path), zoom=zoom)
    
    def highestXG(self):
        topXG = self.data.sort_values(by="xG", ascending=False)
        topXG = topXG[["Rk", "Squad", "xG", "GF"]]
        topXG = topXG.reset_index(drop=True)
        topXG.index += 1
        print(topXG)
        xpoints = topXG["xG"]
        ypoints = topXG["GF"]
        plt.scatter(xpoints, ypoints)

        for x0, y0, squad in zip(xpoints, ypoints, topXG["Squad"]):
            ab = AnnotationBbox(self.getImage(r"C:\Users\ryanw\OneDrive\Documents\GitHub\PLPrediction\BLogos\bayern.gif"), (x0, y0), frameon=False)
            plt.gca().add_artist(ab)
        plt.show()
