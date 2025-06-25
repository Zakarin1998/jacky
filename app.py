from PIL import Image
import qrcode

def generate_qr_with_logo(data, logo_path, output_size=600, logo_ratio=0.2):
    """
    Generate a QR code with a circular logo embedded in the center for a sticker.

    Parameters:
    - data (str): The data to encode in the QR code (e.g., a URL).
    - logo_path (str): Path to the logo image file (100x100 or 600x600 pixels).
    - output_size (int): Desired width/height of the output image in pixels (default: 600).
    - logo_ratio (float): Ratio of logo size to QR code size (default: 0.2, i.e., 20%).

    Returns:
    - None: Saves the image as 'sticker.png'.
    """
    # Step 1: Create the QR code
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        border=4,  # Standard border size in modules
    )
    qr.add_data(data)
    qr.make(fit=True)  # Automatically determine the smallest version that fits the data
    
    # Calculate box_size to approximate the desired output_size
    module_count = qr.modules_count
    total_modules = module_count + 2 * qr.border  # Include border on both sides
    box_size = round(output_size / total_modules)
    qr.box_size = box_size
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Step 2: Prepare the logo
    logo = Image.open(logo_path).convert("RGBA")  # Ensure alpha channel for transparency
    qr_size = qr_img.size[0]  # QR code is square, so width = height
    logo_size = int(qr_size * logo_ratio)  # Resize logo to a fraction of QR code size
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)  # High-quality resizing
    
    # Step 3: Calculate position to center the logo
    pos = ((qr_size - logo_size) // 2, (qr_size - logo_size) // 2)
    
    # Step 4: Overlay the logo onto the QR code
    qr_img.paste(logo, pos, logo)  # Use logo's alpha channel as mask
    
    # Step 5: Save the resulting sticker image
    qr_img.save("sticker.png")
    print(f"Sticker image saved as 'sticker.png' with size {qr_img.size}")

# Example usage
if __name__ == "__main__":
    # Replace with your data and logo path
    sample_data = "https://www.jchandollar.vip"
    sample_logo = "logo_generator/logo_100_100.png"  # Your circular logo (100x100 or 600x600)
    
    # Generate the sticker
    generate_qr_with_logo(
        data=sample_data,
        logo_path=sample_logo,
        output_size=600,  # Final image ~600x600 pixels
        logo_ratio=0.2    # Logo is 20% of QR code size
    )