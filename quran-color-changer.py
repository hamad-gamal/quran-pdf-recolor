#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script:
  1) Converts selected pages of a PDF to images (via pdf2image).
  2) Replaces black (or near-black) pixels with a chosen color (via Pillow/NumPy).
  3) Reassembles those pages into a new PDF.

Default parameters (edit below if not passing via command line):
------------------------------------------------------------------------------
INPUT_PDF     = "D:/quran_hafs_m.pdf"
OUTPUT_PDF    = "D:/0001-quran_hafs_m.pdf"
POPPLER_PATH  = "D:/progs/Release-24.08.0-0/poppler-24.08.0/Library/bin"
COLOR_CHOICE  = 1      # 1..18
THRESHOLD     = 50     # R/G/B < threshold => blackish
DPI           = 200    # resolution for PDF->image conversion
START_PAGE    = 1      # first page to process
END_PAGE      = None   # last page to process (None = process until end)

Color Mapping (choose by number):
  1 : red         -> (255,   0,   0)
  2 : blue        -> (  0,   0, 255)
  3 : green       -> (  0, 255,   0)
  4 : yellow      -> (255, 255,   0)
  5 : orange      -> (255, 165,   0)
  6 : purple      -> (128,   0, 128)
  7 : pink        -> (255, 192, 203)
  8 : cyan        -> (  0, 255, 255)
  9 : magenta     -> (255,   0, 255)
 10 : brown       -> (165,  42,  42)
 11 : Gainsboro   -> (220, 220, 220)
 12 : Light Gray  -> (211, 211, 211)
 13 : Silver      -> (192, 192, 192)
 14 : Dark Gray   -> (169, 169, 169)
 15 : Dim Gray    -> (105, 105, 105)
 16 : White Smoke -> (245, 245, 245)  # very pale grey
 17 : Gray 95%    -> (242, 242, 242)  # near-white grey
 18 : Gray 90%    -> (230, 230, 230)  # slightly darker pale grey
------------------------------------------------------------------------------
"""

import argparse
import os
from pdf2image import convert_from_path
from PIL import Image
import numpy as np
from tqdm import tqdm

# Default parameters
INPUT_PDF = "D:/QURAN/quran_warsh_m.pdf"
OUTPUT_PDF = "D:/QURAN/quran_warsh_WRITING TRAINING.pdf"
POPPLER_PATH  = "D:/progs/Release-24.08.0-0/poppler-24.08.0/Library/bin"
COLOR_CHOICE  = 11
THRESHOLD     = 50
DPI           = 1300
START_PAGE    = 582
END_PAGE      = 604  # None = process through the last page

# Mapping of color choices to RGB tuples
COLOR_CHOICES = {
    1:  (255, 0, 0),       # red
    2:  (0, 0, 255),       # blue
    3:  (0, 255, 0),       # green
    4:  (255, 255, 0),     # yellow
    5:  (255, 165, 0),     # orange
    6:  (128, 0, 128),     # purple
    7:  (255, 192, 203),   # pink
    8:  (0, 255, 255),     # cyan
    9:  (255, 0, 255),     # magenta
    10: (165, 42, 42),     # brown
    11: (220, 220, 220),   # Gainsboro
    12: (211, 211, 211),   # Light Gray
    13: (192, 192, 192),   # Silver
    14: (169, 169, 169),   # Dark Gray
    15: (105, 105, 105),   # Dim Gray
    16: (245, 245, 245),   # White Smoke
    17: (242, 242, 242),   # Gray 95%
    18: (230, 230, 230)    # Gray 90%
}

def replace_black_pixels_with_color(image: Image.Image, target_color=(255, 0, 0), threshold=50) -> Image.Image:
    """
    Replace black or near-black pixels in the given image with the target color.
    Args:
      image (PIL.Image): The input image.
      target_color (tuple): (R, G, B) color for near-black pixels.
      threshold (int): if R/G/B < threshold => blackish pixel.
    Returns:
      PIL.Image: New image where blackish pixels are replaced by target_color.
    """
    # Ensure RGB mode
    image = image.convert("RGB")
    arr = np.array(image, dtype=np.uint8)

    # Create a mask for pixels that are nearly black
    mask = (
        (arr[:, :, 0] < threshold) &
        (arr[:, :, 1] < threshold) &
        (arr[:, :, 2] < threshold)
    )
    # Replace those pixels with target_color
    arr[mask] = target_color

    return Image.fromarray(arr)

def main():
    parser = argparse.ArgumentParser(
        description="Convert a range of PDF pages to images, recolor blackish pixels, rebuild into a PDF."
    )
    parser.add_argument("--input", default=INPUT_PDF, help="Path to the input PDF")
    parser.add_argument("--output", default=OUTPUT_PDF, help="Path to the output PDF")
    parser.add_argument("--poppler-path", default=POPPLER_PATH,
                        help="Path to Poppler bin folder (if not in system PATH)")
    parser.add_argument("--color", type=int, default=COLOR_CHOICE, choices=range(1, 19),
                        help=("Color choice (1..18). e.g., 1=red,2=blue,3=green,4=yellow,5=orange,6=purple,7=pink,"
                              "8=cyan,9=magenta,10=brown,11=Gainsboro,12=LightGray,13=Silver,"
                              "14=DarkGray,15=DimGray,16=WhiteSmoke,17=Gray95%,18=Gray90%"))
    parser.add_argument("--threshold", type=int, default=THRESHOLD,
                        help="Pixel intensity threshold for blackish detection (default=50)")
    parser.add_argument("--dpi", type=int, default=DPI,
                        help="Resolution (DPI) for PDF->image conversion (default=200)")
    parser.add_argument("--start-page", type=int, default=START_PAGE,
                        help="First page to process (1-based). Default=1 (the first page).")
    parser.add_argument("--end-page", type=int, default=END_PAGE,
                        help="Last page to process (1-based). Default=None (through end).")

    args = parser.parse_args()

    # Check input file existence
    if not os.path.isfile(args.input):
        print(f"Input file not found: {args.input}")
        return

    # Determine target color
    target_color = COLOR_CHOICES[args.color]
    if args.color in [11, 12, 13, 16, 17, 18]:
        print("WARNING: A very light grey color has been chosen; it may be barely visible on white paper.")

    # Convert the specified page range to images
    print(f"Converting PDF pages (from page {args.start_page} to {args.end_page or 'end'}) at {args.dpi} DPI...")
    print("Poppler path:", args.poppler_path or "Using system PATH")

    try:
        pages = convert_from_path(
            args.input,
            dpi=args.dpi,
            poppler_path=args.poppler_path,
            first_page=args.start_page,
            last_page=args.end_page
        )
    except Exception as e:
        print("Error converting PDF to images:", e)
        return

    print(f"Loaded {len(pages)} pages. Processing near-black pixels with threshold={args.threshold}...")
    processed_images = []
    for page in tqdm(pages, desc="Replacing black pixels"):
        processed_img = replace_black_pixels_with_color(page, target_color, threshold=args.threshold)
        processed_images.append(processed_img)

    if not processed_images:
        print("No pages were processed. Exiting.")
        return

    # Save the resulting pages into a new PDF
    print("Reassembling processed pages into a new PDF...")
    try:
        processed_images[0].save(
            args.output,
            save_all=True,
            append_images=processed_images[1:]
        )
    except Exception as e:
        print("Error saving output PDF:", e)
        return

    print("Done!")
    print(f"Input PDF      : {args.input}")
    print(f"Output PDF     : {args.output}")
    print(f"Pages processed: {len(processed_images)} (from page {args.start_page} to {args.end_page or 'end'})")

if __name__ == "__main__":
    main()
