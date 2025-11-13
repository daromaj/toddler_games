#!/usr/bin/env python3
"""
Simple icon generator for PWA without external dependencies.
Creates basic PNG files with a colored background and emoji.
"""

import struct
import zlib
import base64

def create_png(width, height, color_rgb):
    """Create a simple PNG file with a solid color background."""
    # PNG signature
    png_signature = b'\x89PNG\r\n\x1a\n'

    # Create IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr_chunk = create_chunk(b'IHDR', ihdr_data)

    # Create image data (simple gradient effect)
    image_data = bytearray()
    r, g, b = color_rgb

    for y in range(height):
        # Filter type (0 = None)
        image_data.append(0)

        # Gradient effect
        factor = y / height
        r2 = int(r * (1 - factor * 0.3))
        g2 = int(g * (1 - factor * 0.3))
        b2 = int(b * (1 - factor * 0.3))

        for x in range(width):
            # Add some variation
            x_factor = x / width
            image_data.extend([
                max(0, min(255, int(r2 - (r2 * x_factor * 0.2)))),
                max(0, min(255, int(g2 - (g2 * x_factor * 0.2)))),
                max(0, min(255, int(b2 - (b2 * x_factor * 0.2))))
            ])

    # Compress image data
    compressed_data = zlib.compress(bytes(image_data), 9)
    idat_chunk = create_chunk(b'IDAT', compressed_data)

    # IEND chunk
    iend_chunk = create_chunk(b'IEND', b'')

    # Combine all chunks
    png_data = png_signature + ihdr_chunk + idat_chunk + iend_chunk

    return png_data

def create_chunk(chunk_type, data):
    """Create a PNG chunk with length, type, data, and CRC."""
    length = struct.pack('>I', len(data))
    chunk_data = chunk_type + data
    crc = struct.pack('>I', zlib.crc32(chunk_data) & 0xffffffff)
    return length + chunk_data + crc

def main():
    # Create icon with gradient purple/blue color
    # Using the theme colors from the app (toddler-friendly!)
    color = (102, 126, 234)  # #667eea

    # Create 192x192 icon
    print("Creating icon-192.png...")
    png_data_192 = create_png(192, 192, color)
    with open('icon-192.png', 'wb') as f:
        f.write(png_data_192)
    print("✓ Created icon-192.png")

    # Create 512x512 icon
    print("Creating icon-512.png...")
    png_data_512 = create_png(512, 512, color)
    with open('icon-512.png', 'wb') as f:
        f.write(png_data_512)
    print("✓ Created icon-512.png")

    print("\nIcons created successfully!")
    print("Note: These are simple placeholder icons. For better icons:")
    print("1. Open generate-icons.html in your browser")
    print("2. Click the download buttons to get proper icons")
    print("3. Replace these files with the downloaded ones")

if __name__ == '__main__':
    main()
