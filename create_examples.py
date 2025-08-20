from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_book_covers():
    """Create sample book covers for testing the application."""
    
    # Create examples directory if it doesn't exist
    os.makedirs("examples", exist_ok=True)
    
    # Book cover configurations
    book_configs = [
        {
            "filename": "fantasy_adventure.png",
            "title": "MAGIC\nQUEST",
            "bg_color": (25, 25, 112),  # Midnight Blue
            "title_color": (255, 215, 0),  # Gold
            "subtitle": "An Epic Adventure",
            "subtitle_color": (255, 255, 255)
        },
        {
            "filename": "mystery_book.png", 
            "title": "THE SECRET\nOF SHADOWS",
            "bg_color": (47, 79, 79),  # Dark Slate Gray
            "title_color": (255, 99, 71),  # Tomato
            "subtitle": "A Mystery Novel",
            "subtitle_color": (220, 220, 220)
        },
        {
            "filename": "childrens_story.png",
            "title": "RAINBOW\nADVENTURES", 
            "bg_color": (135, 206, 250),  # Light Sky Blue
            "title_color": (255, 20, 147),  # Deep Pink
            "subtitle": "A Colorful Journey",
            "subtitle_color": (75, 0, 130)  # Indigo
        },
        {
            "filename": "science_fiction.png",
            "title": "SPACE\nEXPLORER",
            "bg_color": (0, 0, 0),  # Black
            "title_color": (0, 255, 255),  # Cyan
            "subtitle": "Journey to the Stars",
            "subtitle_color": (192, 192, 192)  # Silver
        }
    ]
    
    for config in book_configs:
        create_book_cover(config)
    
    # Create a simple child face example
    create_sample_child_face()
    
    print("✅ Sample images created in 'examples' directory!")

def create_book_cover(config):
    """Create a single book cover with given configuration."""
    
    # Create image
    width, height = 400, 600
    image = Image.new('RGB', (width, height), config["bg_color"])
    draw = ImageDraw.Draw(image)
    
    # Try to use a default font, fallback to default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        subtitle_font = ImageFont.truetype("arial.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Draw title
    title_bbox = draw.textbbox((0, 0), config["title"], font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    title_x = (width - title_width) // 2
    title_y = height // 3
    
    draw.text((title_x, title_y), config["title"], 
              fill=config["title_color"], font=title_font, align="center")
    
    # Draw subtitle
    subtitle_bbox = draw.textbbox((0, 0), config["subtitle"], font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + title_height + 30
    
    draw.text((subtitle_x, subtitle_y), config["subtitle"], 
              fill=config["subtitle_color"], font=subtitle_font)
    
    # Add decorative elements
    # Draw some geometric shapes for visual appeal
    
    # Top border
    draw.rectangle([20, 20, width-20, 40], fill=config["title_color"])
    
    # Bottom border  
    draw.rectangle([20, height-40, width-20, height-20], fill=config["title_color"])
    
    # Side decorations
    for i in range(5):
        y_pos = 80 + i * 100
        draw.ellipse([20, y_pos, 50, y_pos + 30], fill=config["subtitle_color"])
        draw.ellipse([width-50, y_pos, width-20, y_pos + 30], fill=config["subtitle_color"])
    
    # Save the image
    filepath = os.path.join("examples", config["filename"])
    image.save(filepath)
    print(f"Created: {filepath}")

def create_sample_child_face():
    """Create a simple sample child face for testing."""
    
    # Create a simple face illustration
    width, height = 300, 300
    image = Image.new('RGB', (width, height), (255, 220, 177))  # Skin tone
    draw = ImageDraw.Draw(image)
    
    # Face shape (oval)
    face_margin = 50
    draw.ellipse([face_margin, face_margin, width-face_margin, height-face_margin], 
                 fill=(255, 220, 177), outline=(0, 0, 0), width=3)
    
    # Eyes
    eye_y = height // 3
    left_eye_x = width // 3
    right_eye_x = 2 * width // 3
    eye_size = 20
    
    # Left eye
    draw.ellipse([left_eye_x-eye_size, eye_y-10, left_eye_x+eye_size, eye_y+10], 
                 fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw.ellipse([left_eye_x-8, eye_y-5, left_eye_x+8, eye_y+5], fill=(0, 0, 0))
    
    # Right eye  
    draw.ellipse([right_eye_x-eye_size, eye_y-10, right_eye_x+eye_size, eye_y+10], 
                 fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw.ellipse([right_eye_x-8, eye_y-5, right_eye_x+8, eye_y+5], fill=(0, 0, 0))
    
    # Nose
    nose_y = height // 2
    draw.ellipse([width//2-5, nose_y-5, width//2+5, nose_y+5], fill=(255, 200, 160))
    
    # Mouth (smile)
    mouth_y = 2 * height // 3
    draw.arc([width//2-30, mouth_y-15, width//2+30, mouth_y+15], 
             start=0, end=180, fill=(255, 0, 0), width=4)
    
    # Hair
    draw.ellipse([face_margin-10, face_margin-20, width-face_margin+10, height//2], 
                 fill=(139, 69, 19), outline=(101, 67, 33), width=2)
    
    # Save the sample face
    filepath = os.path.join("examples", "sample_child_face.png")
    image.save(filepath)
    print(f"Created: {filepath}")

if __name__ == "__main__":
    create_sample_book_covers()