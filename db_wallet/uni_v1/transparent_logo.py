from PIL import Image

# Load the image
# image_path = "schap_logo.png"
image_path = "hay_logo.png"
image = Image.open(image_path)

# Convert the image to RGBA (if not already in that mode)
image = image.convert("RGBA")

# Create a new image with the same size and a transparent background
transparent_image = Image.new("RGBA", image.size, (0, 0, 0, 0))

# Paste the original image onto the transparent background, keeping only the circular part
width, height = image.size
for x in range(width):
    for y in range(height):
        r, g, b, a = image.getpixel((x, y))
        # Only keep the circular part of the image
        if ((x - width/2)**2 + (y - height/2)**2) <= (min(width, height)/2)**2:
            transparent_image.putpixel((x, y), (r, g, b, a))

# Save the result
output_path = "hay_logo_transparent.png"
transparent_image.save(output_path)

print(output_path)