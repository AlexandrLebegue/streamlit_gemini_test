import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from typing import Optional, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiImageClient:
    """Client for Google Gemini image generation API."""
    
    def __init__(self):
        """Initialize the Gemini client with API key."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure the client
        os.environ["GOOGLE_API_KEY"] = self.api_key
        self.client = genai.Client()
        self.model = "gemini-2.0-flash-preview-image-generation"
    
    def _prepare_image_for_api(self, image: Image.Image, max_size: int = 1024) -> Image.Image:
        """
        Prepare image for API by resizing and converting to RGB format.
        
        Args:
            image: PIL Image object
            max_size: Maximum dimension size
            
        Returns:
            Processed PIL Image object
        """
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large
        width, height = image.size
        if max(width, height) > max_size:
            ratio = max_size / max(width, height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return image
    
    def _create_merge_prompt(self, merge_style: str = "natural") -> str:
        """
        Create a detailed prompt for merging a child's face into a book cover.
        
        Args:
            merge_style: Style of merge ("natural", "artistic", "cartoon")
            
        Returns:
            Generated prompt string
        """
        base_prompt = """I have two images: a child's face photo and a book cover. Please merge the child's face seamlessly into the book cover design. 

Requirements:
- Integrate the child's face naturally into the book cover
- Keep the book's title, text, and design elements intact
- Match the lighting and color tone of the book cover
- Make the face placement look professional and appealing
- Ensure the integration appears natural and well-blended"""

        style_additions = {
            "natural": "Keep the child's face realistic with natural lighting that matches the book cover style.",
            "artistic": "Apply artistic effects to blend the face with the book's illustration style while keeping it recognizable.",
            "cartoon": "Stylize the face to match cartoon or illustrated book aesthetics if the cover has that style."
        }
        
        return f"{base_prompt}\n- {style_additions.get(merge_style, style_additions['natural'])}\n\nGenerate the merged book cover image with the child's face integrated."
    
    def merge_face_into_book_cover(
        self, 
        face_image: Image.Image, 
        book_cover_image: Image.Image,
        merge_style: str = "natural"
    ) -> Optional[Image.Image]:
        """
        Merge a child's face into a book cover using Gemini image generation API.
        
        Args:
            face_image: PIL Image of the child's face
            book_cover_image: PIL Image of the book cover
            merge_style: Style of merge ("natural", "artistic", "cartoon")
            
        Returns:
            Generated merged image as PIL Image or None if failed
        """
        try:
            # Prepare images for API
            face_img = self._prepare_image_for_api(face_image)
            book_img = self._prepare_image_for_api(book_cover_image)
            
            # Create prompt
            prompt = self._create_merge_prompt(merge_style)
            
            # Generate content with both images
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents=[prompt, face_img, book_img],
                config=types.GenerateContentConfig(
                    response_modalities=['IMAGE']
                )
            )
            
            # Extract the generated image
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    generated_image = Image.open(BytesIO(part.inline_data.data))
                    return generated_image
            
            return None
            
        except Exception as e:
            print(f"Error generating merged image: {str(e)}")
            return None
    
    def analyze_images(self, face_image: Image.Image, book_cover_image: Image.Image) -> str:
        """
        Analyze both images to provide merge suggestions using text generation.
        
        Args:
            face_image: PIL Image of the child's face
            book_cover_image: PIL Image of the book cover
            
        Returns:
            Analysis text with suggestions
        """
        try:
            face_img = self._prepare_image_for_api(face_image)
            book_img = self._prepare_image_for_api(book_cover_image)
            
            prompt = """Analyze these two images for face merging:
1. First image: A child's face photo
2. Second image: A book cover

Provide brief suggestions on:
- Best placement for the face on the book cover
- Color/lighting adjustments needed
- Style compatibility
- Any potential challenges

Keep the analysis concise and practical."""

            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",  # Use text model for analysis
                contents=[prompt, face_img, book_img],
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT']
                )
            )
            
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    return part.text
            
            return "Unable to analyze images."
            
        except Exception as e:
            return f"Error analyzing images: {str(e)}"
    
    def validate_images(self, face_image: Image.Image, book_cover_image: Image.Image) -> Tuple[bool, str]:
        """
        Validate if images are suitable for merging.
        
        Args:
            face_image: PIL Image of the child's face
            book_cover_image: PIL Image of the book cover
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Basic validation
            if face_image.size[0] < 100 or face_image.size[1] < 100:
                return False, "Face image is too small (minimum 100x100 pixels)"
            
            if book_cover_image.size[0] < 200 or book_cover_image.size[1] < 200:
                return False, "Book cover image is too small (minimum 200x200 pixels)"
            
            # Check file size (approximate)
            face_bytes = BytesIO()
            face_image.save(face_bytes, format='JPEG')
            if len(face_bytes.getvalue()) > 10 * 1024 * 1024:  # 10MB limit
                return False, "Face image file is too large (max 10MB)"
            
            book_bytes = BytesIO()
            book_cover_image.save(book_bytes, format='JPEG')
            if len(book_bytes.getvalue()) > 10 * 1024 * 1024:  # 10MB limit
                return False, "Book cover image file is too large (max 10MB)"
            
            return True, "Images are suitable for merging"
            
        except Exception as e:
            return False, f"Error validating images: {str(e)}"
    
    def test_api_connection(self) -> Tuple[bool, str]:
        """
        Test if the API connection is working.
        
        Returns:
            Tuple of (is_connected, message)
        """
        try:
            # Create a simple test image
            test_image = Image.new('RGB', (100, 100), color='red')
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=["What color is this image?", test_image],
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT']
                )
            )
            
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    return True, "API connection successful"
            
            return False, "API connection failed - no response"
            
        except Exception as e:
            return False, f"API connection failed: {str(e)}"