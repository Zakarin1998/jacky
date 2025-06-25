from qrcode import QRCode

def test_setup_position_probe_pattern(qr:QRCode, row, col):
    """
    Test the setup of position probe patterns at (row, col).
    
    The setup_position_probe_pattern method sets up the large squares in the QR code corners. This function tests its placement logic.
    """
    qr.modules = [[None] * qr.modules_count for _ in range(qr.modules_count)]  # Reset modules
    qr.setup_position_probe_pattern(row, col)
    print(f"Position probe pattern at ({row}, {col}):")
    for r in range(max(0, row - 1), min(qr.modules_count, row + 8)):
        for c in range(max(0, col - 1), min(qr.modules_count, col + 8)):
            state = qr.modules[r][c]
            print(f"Module ({r}, {c}): {'True' if state else 'False'}")


def test_best_fit(qr:QRCode, data_str):
    """
    Test the best_fit method with given data.
    
    The best_fit method calculates the smallest QR code version for the data. This function verifies its logic.
    """
    qr.add_data(data_str)
    version = qr.best_fit()
    print(f"Data: '{data_str}' -> Best fit version: {version}")
    return version


def test_best_mask_pattern(qr:QRCode):
    """Test the selection of the best mask pattern."""
    qr.add_data("Test data")
    qr.make()  # Generate the QR code
    pattern = qr.best_mask_pattern()
    print(f"Best mask pattern: {pattern}")
    return pattern


def test_make_image(qr:QRCode, data_str, filename="test_qr.png"):
    """Test QR code image generation."""
    qr.add_data(data_str)
    qr.make()
    image = qr.make_image()
    image.save(filename)
    print(f"QR code image saved as '{filename}'")
    return image


def test_map_data(qr:QRCode, data_str, mask_pattern=0):
    """Test data mapping into the QR code matrix."""
    qr.add_data(data_str)
    qr.make()  # Ensure data_cache is populated
    qr.modules = [[None] * qr.modules_count for _ in range(qr.modules_count)]  # Reset modules
    qr.map_data(qr.data_cache, mask_pattern)
    print(f"Module state after mapping with mask {mask_pattern}:")
    for r in range(qr.modules_count):
        for c in range(qr.modules_count):
            if qr.modules[r][c] is not None:
                print(f"Module ({r}, {c}): {qr.modules[r][c]}")
