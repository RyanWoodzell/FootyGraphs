from PIL import Image
from collections import Counter
import os

def top_two_prevalent_rgb(image_path):
    # Open the image
    img = Image.open(image_path)
    # Resize the image to simplify the analysis
    img = img.resize((50, 50))  # Small size to reduce processing time
    # Convert the image to RGB
    img = img.convert("RGB")
    # Get all pixels
    pixels = list(img.getdata())
    # Count the frequency of each RGB value
    counter = Counter(pixels)
    # Get the two most common RGB values
    top_two_colors = counter.most_common(2)
    return top_two_colors

def rgb_to_hex(rgb):
    # Convert an RGB tuple to a hexadecimal string
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

# Folder containing Bundesliga logos
logos_folder = "BLogos"

# Dictionary to store results
team_colors = {}

# Iterate over each image in the folder
for filename in os.listdir(logos_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        team_name = os.path.splitext(filename)[0]  # Get the team name
        image_path = os.path.join(logos_folder, filename)
        top_colors = top_two_prevalent_rgb(image_path)
        # Get the RGB and Hex values for the top two colors
        most_common_rgb, most_common_count = top_colors[0]
        second_common_rgb, second_common_count = top_colors[1]
        team_colors[team_name] = {
            "most_common": rgb_to_hex(most_common_rgb),
            "second_common": rgb_to_hex(second_common_rgb)
        }

# Print the results
for team, colors in team_colors.items():
    print(f"{team}: Most Common: {colors['most_common']}, Second Most Common: {colors['second_common']}")
