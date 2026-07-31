#!/usr/bin/env python3
"""Check CPHO41-Q02 paper page images for dimensions and basic info."""
import struct, sys, os

def png_dimensions(path):
    """Read PNG dimensions from file header."""
    with open(path, 'rb') as f:
        sig = f.read(8)
        if sig != b'\x89PNG\r\n\x1a\n':
            print(f"  Not a valid PNG: {path}")
            return None
        f.read(4)  # chunk length
        f.read(4)  # chunk type (IHDR)
        width = struct.unpack('>I', f.read(4))[0]
        height = struct.unpack('>I', f.read(4))[0]
        bit_depth = ord(f.read(1))
        color_type = ord(f.read(1))
        return {
            'width': width,
            'height': height,
            'bit_depth': bit_depth,
            'color_type': color_type,
            'file_size': os.path.getsize(path),
        }

for path in [
    "/Users/dongxingxi/physics_competition_thesis_excellent_v2/03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q02-paper-page-1.png",
    "/Users/dongxingxi/physics_competition_thesis_excellent_v2/03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q02-paper-page-2.png",
]:
    if os.path.exists(path):
        info = png_dimensions(path)
        print(f"\n=== {os.path.basename(path)} ===")
        if info:
            print(f"  Dimensions: {info['width']}x{info['height']} px")
            print(f"  File size: {info['file_size'] / 1024:.1f} KB")
            print(f"  Bit depth: {info['bit_depth']}")
            print(f"  Color type: {info['color_type']} (2=RGB, 6=RGBA)")
    else:
        print(f"\n=== FILE NOT FOUND: {path} ===")
