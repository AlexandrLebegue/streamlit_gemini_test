import streamlit as st
import io
import base64
from PIL import Image
from gemini_client import GeminiImageClient
import os
from typing import Optional

# Configure Streamlit page
st.set_page_config(
    page_title="AI Book Cover Face Merger",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'gemini_client' not in st.session_state:
    st.session_state.gemini_client = None
if 'face_image' not in st.session_state:
    st.session_state.face_image = None
if 'book_image' not in st.session_state:
    st.session_state.book_image = None
if 'merged_image' not in st.session_state:
    st.session_state.merged_image = None

def initialize_gemini_client():
    """Initialize the Gemini client with error handling."""
    try:
        if st.session_state.gemini_client is None:
            st.session_state.gemini_client = GeminiImageClient()
        return True, "Gemini client initialized successfully"
    except ValueError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Error initializing Gemini client: {str(e)}"

def validate_uploaded_image(uploaded_file, image_type: str) -> tuple[bool, str, Optional[Image.Image]]:
    """
    Validate and process uploaded image file.
    
    Args:
        uploaded_file: Streamlit uploaded file
        image_type: Type of image ("face" or "book")
        
    Returns:
        Tuple of (is_valid, message, image)
    """
    if uploaded_file is None:
        return False, f"Please upload a {image_type} image", None
    
    # Check file type
    if uploaded_file.type not in ["image/jpeg", "image/jpg", "image/png"]:
        return False, "Please upload a JPEG or PNG image", None
    
    # Check file size (10MB limit)
    if uploaded_file.size > 10 * 1024 * 1024:
        return False, "File size too large. Please upload an image smaller than 10MB", None
    
    try:
        image = Image.open(uploaded_file)
        
        # Basic validation
        if image.size[0] < 100 or image.size[1] < 100:
            min_size = "100x100" if image_type == "face" else "200x200"
            return False, f"{image_type.title()} image too small. Minimum size: {min_size} pixels", None
        
        return True, f"{image_type.title()} image uploaded successfully", image
        
    except Exception as e:
        return False, f"Error processing {image_type} image: {str(e)}", None

def create_download_link(image: Image.Image, filename: str) -> str:
    """Create a download link for the generated image."""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    img_data = buffer.getvalue()
    b64 = base64.b64encode(img_data).decode()
    return f'<a href="data:image/png;base64,{b64}" download="{filename}">Download Merged Image</a>'

def main():
    """Main application function."""
    
    # Header
    st.title("📚 AI Book Cover Face Merger")
    st.markdown("Merge a child's face seamlessly into book cover artwork using AI")
    
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        st.error("⚠️ GEMINI_API_KEY not found. Please set up your environment variables.")
        st.info("Create a `.env` file with your Gemini API key: `GEMINI_API_KEY=your_key_here`")
        return
    
    # Initialize Gemini client
    client_ok, client_msg = initialize_gemini_client()
    if not client_ok:
        st.error(f"❌ {client_msg}")
        return
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Merge style selection
        merge_style = st.selectbox(
            "Merge Style",
            ["natural", "artistic", "cartoon"],
            help="Choose how the face should be integrated into the book cover"
        )
        
        # API connection test
        if st.button("🔗 Test API Connection"):
            with st.spinner("Testing API connection..."):
                is_connected, connection_msg = st.session_state.gemini_client.test_api_connection()
                if is_connected:
                    st.success(f"✅ {connection_msg}")
                else:
                    st.error(f"❌ {connection_msg}")
    
    # Main content area
    col1, col2 = st.columns(2)
    
    # Left column - Face image upload
    with col1:
        st.subheader("👶 Child's Face Image")
        face_file = st.file_uploader(
            "Upload child's face photo",
            type=["png", "jpg", "jpeg"],
            key="face_upload",
            help="Upload a clear photo of the child's face"
        )
        
        if face_file:
            is_valid, msg, face_img = validate_uploaded_image(face_file, "face")
            if is_valid:
                st.success(msg)
                st.session_state.face_image = face_img
                st.image(face_img, caption="Child's Face", use_column_width=True)
            else:
                st.error(msg)
                st.session_state.face_image = None
    
    # Right column - Book cover upload
    with col2:
        st.subheader("📖 Book Cover Image")
        book_file = st.file_uploader(
            "Upload book cover image",
            type=["png", "jpg", "jpeg"],
            key="book_upload",
            help="Upload the book cover where you want to merge the face"
        )
        
        if book_file:
            is_valid, msg, book_img = validate_uploaded_image(book_file, "book")
            if is_valid:
                st.success(msg)
                st.session_state.book_image = book_img
                st.image(book_img, caption="Book Cover", use_column_width=True)
            else:
                st.error(msg)
                st.session_state.book_image = None
    
    # Analysis section
    if st.session_state.face_image and st.session_state.book_image:
        st.divider()
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🔍 Analyze Images", use_container_width=True):
                with st.spinner("Analyzing images..."):
                    analysis = st.session_state.gemini_client.analyze_images(
                        st.session_state.face_image, 
                        st.session_state.book_image
                    )
                    st.info(f"📋 **Analysis:**\n{analysis}")
        
        with col2:
            if st.button("✅ Validate Images", use_container_width=True):
                with st.spinner("Validating images..."):
                    is_valid, validation_msg = st.session_state.gemini_client.validate_images(
                        st.session_state.face_image,
                        st.session_state.book_image
                    )
                    if is_valid:
                        st.success(f"✅ {validation_msg}")
                    else:
                        st.warning(f"⚠️ {validation_msg}")
        
        with col3:
            if st.button("🎨 Generate Merge", use_container_width=True, type="primary"):
                if st.session_state.gemini_client:
                    with st.spinner("Generating merged image... This may take a few moments"):
                        merged_image = st.session_state.gemini_client.merge_face_into_book_cover(
                            st.session_state.face_image,
                            st.session_state.book_image,
                            merge_style
                        )
                        
                        if merged_image:
                            st.session_state.merged_image = merged_image
                            st.success("🎉 Image merged successfully!")
                        else:
                            st.error("❌ Failed to generate merged image. Please try again.")
    
    # Results section
    if st.session_state.merged_image:
        st.divider()
        st.subheader("🎨 Generated Result")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.image(
                st.session_state.merged_image, 
                caption="Merged Book Cover", 
                use_column_width=True
            )
        
        with col2:
            st.markdown("### 📥 Download")
            
            # Create download button
            img_buffer = io.BytesIO()
            st.session_state.merged_image.save(img_buffer, format="PNG")
            
            st.download_button(
                label="💾 Download Image",
                data=img_buffer.getvalue(),
                file_name="merged_book_cover.png",
                mime="image/png",
                use_container_width=True
            )
            
            # Reset button
            if st.button("🔄 Create Another", use_container_width=True):
                st.session_state.merged_image = None
                st.rerun()
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            Made with ❤️ using Streamlit and Google Gemini AI<br>
            <small>Upload clear, high-quality images for best results</small>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()