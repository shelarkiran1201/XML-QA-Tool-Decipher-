"""
Icon Generator for Survey QA Validator
This script creates a simple application icon in .ico format
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a 256x256 image with a gradient background
    size = 256
    img = Image.new('RGB', (size, size), color='#0e7c3d')
    draw = ImageDraw.Draw(img)
    
    # Draw a gradient background
    for i in range(size):
        shade = int(14 + (124 - 14) * (i / size))
        color = f'#{shade:02x}7c3d'
        draw.line([(0, i), (size, i)], fill=color)
    
    # Draw a document icon representation
    # White rounded rectangle for document
    margin = 40
    doc_left = margin
    doc_top = margin
    doc_right = size - margin
    doc_bottom = size - margin
    
    # Document background
    draw.rounded_rectangle(
        [(doc_left, doc_top), (doc_right, doc_bottom)],
        radius=20,
        fill='white',
        outline='#1e1e1e',
        width=4
    )
    
    # Draw "QA" text
    try:
        # Try to use a nice font, fallback to default if not available
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    text = "QA"
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 - 10
    
    # Draw text with shadow
    draw.text((text_x + 2, text_y + 2), text, fill='#cccccc', font=font)
    draw.text((text_x, text_y), text, fill='#0e7c3d', font=font)
    
    # Draw checkmark
    check_size = 30
    check_x = size - margin - 30
    check_y = doc_bottom - 50
    
    draw.line([(check_x - check_size//2, check_y), 
               (check_x - check_size//4, check_y + check_size//2)],
              fill='#0e7c3d', width=6)
    draw.line([(check_x - check_size//4, check_y + check_size//2),
               (check_x + check_size//2, check_y - check_size//2)],
              fill='#0e7c3d', width=6)
    
    # Save as ICO with multiple sizes
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save('app_icon.ico', format='ICO', sizes=icon_sizes)
    print("✓ Icon created successfully: app_icon.ico")
    print(f"  Sizes included: {', '.join([f'{s[0]}x{s[1]}' for s in icon_sizes])}")

if __name__ == "__main__":
    create_icon()
