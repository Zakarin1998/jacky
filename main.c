#include <stdio.h>
#include <stdlib.h>
#include <qrencode.h>

int main() {
    const char *url = "https://jchandollar.vip";
    
    // Encode the string into QR code with default settings
    QRcode *qrcode = QRcode_encodeString(
        url,                   // your URL
        0,                     // version 0 = auto
        QR_ECLEVEL_L,          // Error correction level (L = lowest)
        QR_MODE_8,             // 8-bit mode for URLs
        1                      // case-sensitive (1 = true)
    );

    if (!qrcode) {
        fprintf(stderr, "QR code encoding failed.\n");
        return 1;
    }

    // Print as ASCII for demonstration
    for (int y = 0; y < qrcode->width; y++) {
        for (int x = 0; x < qrcode->width; x++) {
            unsigned char b = qrcode->data[y * qrcode->width + x] & 1;
            printf(b ? "██" : "  ");
        }
        printf("\n");
    }

    QRcode_free(qrcode);
    return 0;
}
