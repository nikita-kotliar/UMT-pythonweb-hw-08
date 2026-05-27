import cloudinary
import cloudinary.uploader
from src.conf.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


def upload_avatar(file_bytes: bytes, public_id: str) -> str:
    """Upload avatar to Cloudinary and return the secure URL."""
    result = cloudinary.uploader.upload(
        file_bytes,
        public_id=f"avatars/{public_id}",
        overwrite=True,
        transformation=[{"width": 250, "height": 250, "crop": "fill"}],
    )
    return result["secure_url"]
