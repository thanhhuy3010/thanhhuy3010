import action_profile_builder
from PIL import Image

# Ghi đè hàm tải ảnh bằng hàm đọc file nội bộ
def mock_fetch_image_as_pil(url):
    try:
        return Image.open("/Users/tranhuy/Downloads/IMG_7527.jpg")
    except Exception as e:
        print(f"Error opening local image: {e}")
        return None

action_profile_builder.fetch_image_as_pil = mock_fetch_image_as_pil
action_profile_builder.create_svg()
