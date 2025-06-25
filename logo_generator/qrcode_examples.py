import qrcode

from qrcode_wrap import (
    test_map_data,
    test_best_fit,
    test_best_mask_pattern,
    test_make_image,
    test_setup_position_probe_pattern
)


# 1. Test Position Probe Patterns
qr = qrcode.QRCode(version=1, border=4)
test_setup_position_probe_pattern(qr, 0, 0)  # Test top-left corner
# Expected Output: A 7x7 square with borders and a 3x3 center set to True, surrounded by False.


# 2. Test Best Fit Version
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
test_best_fit(qr, "Hello, World!")
test_best_fit(qr, "A longer string to test version increase")
# Expected Output: Version numbers (e.g., 1, 2) that increase with data length.



# 3. Test Mask Pattern Selection
# The best_mask_pattern method chooses the optimal mask. This function tests its selection process.
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
test_best_mask_pattern(qr)
# Expected Output: A number between 0 and 7 representing the chosen mask.


# 4. Test Image Generation
# The make_image method creates a QR code image. This function tests its output.
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
test_make_image(qr, "https://example.com")
# Verification: Open test_qr.png and scan it with a QR reader to confirm the data.


# 5. Test Module Mapping
# The map_data method places data bits into the matrix. This function inspects the resulting pattern.
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
test_map_data(qr, "Test")
# Expected Output: A list of module states showing the zigzag data placement.
