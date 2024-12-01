from PIL import Image
import os

# Folder paths
input_folder = "BLogos1"
output_folder = "BLogos"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Desired size
new_width = 500  # Replace with your desired width
new_height = 500  # Replace with your desired height

for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)
        img_resized = img.resize((new_width, new_height))
        img_resized.save(os.path.join(output_folder, filename))

print("All images have been resized!")
