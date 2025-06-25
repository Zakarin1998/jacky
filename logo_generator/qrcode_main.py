# Testing the Entire QR Code Generation Process
# To test the full workflow, combine these functions into a complete example:
import qrcode
from qrcode_wrap import (
    test_setup_position_probe_pattern,
    test_make_image,
    test_best_fit,
    test_best_mask_pattern,
    test_map_data
)

# Initialize QRCode
qr = qrcode.QRCode(
    version=None,  # Auto-determined
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4
)

# Add data
data = "https://jchandollar.vip"
qr.add_data(data)

# Test individual components
print("Testing position probe pattern:")
test_setup_position_probe_pattern(qr, 0, 0)

print("\nTesting best fit:")
version = test_best_fit(qr, data)

print("\nTesting mask pattern:")
mask = test_best_mask_pattern(qr)

# Generate QR code
qr.make()

# Test image generation
test_make_image(qr, data, "output_qr.png")

# Print to terminal for visual inspection
qr.print_ascii()

