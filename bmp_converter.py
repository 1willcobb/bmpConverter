import os
from PIL import Image, ExifTags

# Relative paths for the input and output directories
input_directory = "input"
output_directory = "output"

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Get the absolute path to the script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Get the absolute paths for the input and output directories
input_directory = os.path.join(script_directory, input_directory)
output_directory = os.path.join(script_directory, output_directory)

# Iterate through the files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.JPG', '.PNG', '.JPEG')):  # Filter for image files
        input_image_path = os.path.join(input_directory, filename)
        output_image_path = os.path.join(output_directory, filename)

        # Open the image using Pillow
        image = Image.open(input_image_path)

        # Check for and correct the orientation if needed
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                try:
                    exif = dict(image._getexif().items())
                    if exif[orientation] == 3:
                        image = image.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        image = image.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        image = image.rotate(90, expand=True)
                except (AttributeError, KeyError, IndexError):
                    # No EXIF orientation data, ignore
                    pass

        # Determine the original width and height
        original_width, original_height = image.size

        # Check if the image is in landscape orientation (horizontal)
        if original_width <= original_height:
            print(f"Processing: {filename} (portrait)")

            # Calculate the scaling factor for height
            height_scale = 480 / original_height
            new_width = int(original_width * height_scale)

            # Create a blank canvas of screen dimensions
            background = Image.new('1', (800, 480), 1)

            # Calculate the position to center the resized image on the canvas
            x_offset = (800 - new_width) // 2

            # Resize and paste the image onto the canvas with white space on the sides
            image = image.resize((new_width, 480), Image.LANCZOS)
            background.paste(image, (x_offset, 0))

            # Save the 1-bit BMP image
            background.save(output_image_path, "BMP")
        else:
            print(f"Processing: {filename} (landscape)")

            # Resize the image to 800x480 pixels
            image = image.resize((800, 480), Image.LANCZOS)

            # Convert the image to 1-bit (black and white)
            image = image.convert("1")

            # Save the 1-bit BMP image
            image.save(output_image_path, "BMP")

        print(f"Processed: {filename}")

print("Conversion of all images is complete.")
